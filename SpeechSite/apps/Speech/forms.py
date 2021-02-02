from django import forms

language_model_choices = ((1,'ru simple'), (2,'ru hard'), (3,'en simple'), (4,'en hard'))

class SelectForm(forms.Form):
    language_model = forms.ChoiceField(choices = language_model_choices)
