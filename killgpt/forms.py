from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class TextInputForm(forms.Form):
    text_input = forms.CharField( widget=forms.Textarea(attrs={'rows': 8, 'cols': 40, 'class': 'custom-field', 'label': 'Input your text here.', 'style': 'background-color: #282D64; border-color: white; color: white;'} ))
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-lg-2'
    #     self.helper.field_class = 'col-lg-8'
    #     self.helper.layout = Layout(
            
    #         Submit('submit', 'Submit', css_class='btn btn-primary'),
    #     )
     

# class TextInputForm(forms.Form):
#     text_input = forms.TextField()
    
