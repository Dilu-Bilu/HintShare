from .models import Comment
from django import forms

OPTIONS = (
    ("l", "likes"),
    ("d","date created"),
   
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control' }),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class SortForm(forms.Form):
    sort_method = forms.ChoiceField(widget=forms.RadioSelect,
                                         choices=OPTIONS)