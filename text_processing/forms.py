from django import forms
from django.forms import Form


class TextProcessingForm(Form):
    file = forms.FileField()
