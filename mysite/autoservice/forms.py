from django import forms
from .models import Komentaras


class UzsakymasKomentarasForm(forms.ModelForm):
    class Meta:
        model = Komentaras
        fields = ("uzsakymas", "vartotojas", "tekstas")
        widgets = {"uzsakymas": forms.HiddenInput(), "vartotojas": forms.HiddenInput()}
