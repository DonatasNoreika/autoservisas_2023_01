from django import forms
from .models import Komentaras, Profilis
from django.contrib.auth.models import User


class UzsakymasKomentarasForm(forms.ModelForm):
    class Meta:
        model = Komentaras
        fields = ("uzsakymas", "vartotojas", "tekstas")
        widgets = {"uzsakymas": forms.HiddenInput(), "vartotojas": forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']