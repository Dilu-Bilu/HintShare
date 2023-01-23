from django.shortcuts import render

# Create your views here.
import numpy as np
import torch
import time
from pytorch_pretrained_bert import (GPT2LMHeadModel, GPT2Tokenizer)
import unicodedata
from .forms import TextInputForm

class AbstractLanguageChecker():
    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

    def check_probabilities(self, in_text, topk=40):
        raise NotImplementedError

    def postprocess(self, token):
        raise NotImplementedError


class LM(AbstractLanguageChecker):
    def __init__(self, model_name_or_path="gpt2"):
        super(LM, self).__init__()
        self.enc = GPT2Tokenizer.from_pretrained(model_name_or_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.model.eval()
        self.start_token = '<|endoftext|>'
        print("Loaded GPT-2 model!")

    def check_probabilities(self, in_text, topk=40):
        # Process input
        start_t = torch.full((1, 1),
                             self.enc.encoder[self.start_token],
                             device=self.device,
                             dtype=torch.long)
        context = self.enc.encode(in_text)
        context = torch.tensor(context,
                               device=self.device,
                               dtype=torch.long).unsqueeze(0)
        context = torch.cat([start_t, context], dim=1)
        # Forward through the model
        logits, _ = self.model(context)

        # construct target and pred
        yhat = torch.softmax(logits[0, :-1], dim=-1)
        y = context[0, 1:]
        # Sort the predictions for each timestep
        sorted_preds = np.argsort(-yhat.data.cpu().numpy())
        # [(pos, prob), ...]
        real_topk_pos = list(
            [int(np.where(sorted_preds[i] == y[i].item())[0][0])
             for i in range(y.shape[0])])
        real_topk_probs = yhat[np.arange(
            0, y.shape[0], 1), y].data.cpu().numpy().tolist()
        real_topk_probs = list(map(lambda x: round(x, 5), real_topk_probs))

        real_topk = list(zip(real_topk_pos, real_topk_probs))
        # [str, str, ...]
        bpe_strings = [self.enc.decoder[s.item()] for s in context[0]]

        bpe_strings = [self.postprocess(s) for s in bpe_strings]

        # [[(pos, prob), ...], [(pos, prob), ..], ...]
        pred_topk = [
            list(zip([self.enc.decoder[p] for p in sorted_preds[i][:topk]],
                     list(map(lambda x: round(x, 5),
                              yhat[i][sorted_preds[i][
                                      :topk]].data.cpu().numpy().tolist()))))
            for i in range(y.shape[0])]

        pred_topk = [[(self.postprocess(t[0]), t[1]) for t in pred] for pred in pred_topk]
        payload = {'bpe_strings': bpe_strings,
                   'real_topk': real_topk,
                   'pred_topk': pred_topk}
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return payload

    def postprocess(self, token):
        with_space = False
        with_break = False
        if token.startswith('Ġ'):
            with_space = True
            token = token[1:]
            # print(token)
        elif token.startswith('â'):
            token = ' '
        elif token.startswith('Ċ'):
            token = ' '
            with_break = True

        token = '-' if token.startswith('â') else token
        token = '“' if token.startswith('ľ') else token
        token = '”' if token.startswith('Ŀ') else token
        token = "'" if token.startswith('Ļ') else token

        if with_space:
            token = '\u0120' + token
        if with_break:
            token = '\u010A' + token

        return token


def humanity_score(final):
    score = (10* final[1]/final[0] + 30 * (final[2]/final[0]) + 100 * (final[3]/final[0]))
    return score 

def main_code(raw_text):
    final = []
    raw_text = unicodedata.normalize("NFKD", raw_text).encode("ascii", "ignore").decode("utf-8")
    lm = LM()
    payload = lm.check_probabilities(raw_text, topk=5)
    # Print out the number of the different k values  
    real_topk = np.array(payload["real_topk"])

    final = [np.count_nonzero(real_topk[:, 0] < 10),
            np.count_nonzero((real_topk[:, 0] < 100) & (real_topk[:, 0] >= 10)),
            np.count_nonzero((real_topk[:, 0] < 1000) & (real_topk[:, 0] >= 100)),
            np.count_nonzero(real_topk[:, 0] >= 1000)
            ]
    return final
  

# Input all your text into this. The input() function is not used because it can only take a certain number of words. Also you can put it into hte input string 
# The function cannot take in quotation marks as inputs. So we parse them out with the remove_quotation_marks 


def limit_string_size(string):
    word_list = string.split(" ")
    limited_string = " ".join(word_list[:500])
    return limited_string


def TextInputView(request):
    form = TextInputForm()
    output = None
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text_input']
            input_text = limit_string_size(text)
            input_text = unicodedata.normalize("NFKD", input_text).encode("ascii", "ignore").decode("utf-8")
            output_list = main_code(input_text)
            score = humanity_score(output_list)
            if score > 7: 
                decision = "This seems to be human text."
            else: 
                decision = "This text is most likely AI generated."
        context = {'form': form, 'output': output_list, 'score': score, 'decision': decision}
    else: 
        context = {'form': form}
    return render(request, 'killgpt/forms.html', context)
