from django import forms

from .pesel import Pesel


class PeselForm(forms.Form):
    pesel = forms.CharField(max_length=11)

    def clean_pesel(self) -> str:
        pesel = self.cleaned_data.get("pesel")
        try:
            Pesel(pesel)
        except ValueError as e:
            raise forms.ValidationError(e)
        return pesel
