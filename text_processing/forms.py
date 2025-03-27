from django import forms
from django.forms import Form


class TextProcessingForm(Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control", "id": "formFile"}
        )
    )
