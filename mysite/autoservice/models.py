from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
from tinymce.models import HTMLField

utc = pytz.UTC


# Create your models here.
class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name="Markė", max_length=100)
    modelis = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilio modeliai'


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(verbose_name="Valstybinis numeris", max_length=100)
    vin_kodas = models.CharField(verbose_name="VIN kodas", max_length=100)
    klientas = models.CharField(verbose_name="Klientas", max_length=100)
    automobilio_modelis = models.ForeignKey(to=AutomobilioModelis, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField('Nuotrauka', upload_to='automobiliai', null=True)
    aprasymas = HTMLField(verbose_name="Aprašymas", null=True, blank=True)

    def __str__(self):
        return f"{self.automobilio_modelis} ({self.valstybinis_nr})"

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'


class Paslauga(models.Model):
    pavadinimas = models.CharField(verbose_name="Pavadinimas", max_length=100)
    kaina = models.FloatField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.pavadinimas}"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Uzsakymas(models.Model):
    data = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    terminas = models.DateTimeField(verbose_name="Terminas", null=True)
    automobilis = models.ForeignKey(to="Automobilis", on_delete=models.CASCADE)
    vartotojas = models.ForeignKey(to=User, verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True, blank=True)

    def ar_praejo_terminas(self):
        if self.terminas:
            return self.terminas.replace(tzinfo=utc) < datetime.datetime.today().replace(tzinfo=utc)
        else:
            return False

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atšaukta'),
        ('i', 'Įvykdyta'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text='Statusas',
    )

    def suma(self):
        suma = 0
        eilutes = self.eilutes.all()
        for eilute in eilutes:
            suma += eilute.kaina()
        return suma

    def __str__(self):
        return f"{self.automobilis} ({self.terminas})"

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", on_delete=models.CASCADE, related_name="eilutes")
    paslauga = models.ForeignKey(to="Paslauga", on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name="Kiekis")

    def kaina(self):
        return self.paslauga.kaina * self.kiekis

    def __str__(self):
        return f"{self.uzsakymas.data}, {self.paslauga} ({self.kiekis})"

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'


class Komentaras(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="komentarai")
    vartotojas = models.ForeignKey(to=User, verbose_name="Vartotojas", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    tekstas = models.TextField(verbose_name="Tekstas", max_length=1000)

    class Meta:
        verbose_name = 'Komentaras'
        verbose_name_plural = 'Komentarai'
        ordering = ['-date_created']
