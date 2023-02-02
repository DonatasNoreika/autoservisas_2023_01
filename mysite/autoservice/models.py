from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

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
    data = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    terminas = models.DateTimeField(verbose_name=_("Deadline"), null=True)
    automobilis = models.ForeignKey(to="Automobilis", verbose_name=_("Vehicle"), on_delete=models.CASCADE)
    vartotojas = models.ForeignKey(to=User, verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)

    def ar_praejo_terminas(self):
        if self.terminas:
            return self.terminas.replace(tzinfo=utc) < datetime.datetime.today().replace(tzinfo=utc)
        else:
            return False

    LOAN_STATUS = (
        ('p', _('Confirmed')),
        ('v', _('In Progress')),
        ('a', _('Canceled')),
        ('i', _('Done')),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text=_("Status"),
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
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-data']


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", verbose_name=_("Order") , on_delete=models.CASCADE, related_name="eilutes")
    paslauga = models.ForeignKey(to="Paslauga", verbose_name=_("Service"), on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name=_("Quantity"))

    def kaina(self):
        return self.paslauga.kaina * self.kiekis

    def __str__(self):
        return f"{self.uzsakymas.data}, {self.paslauga} ({self.kiekis})"

    class Meta:
        verbose_name = _("Orderline")
        verbose_name_plural = _("Orderlines")


class Komentaras(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", verbose_name="Užsakymas", on_delete=models.CASCADE, null=True, blank=True, related_name="komentarai")
    vartotojas = models.ForeignKey(to=User, verbose_name="Vartotojas", on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tekstas = models.TextField(verbose_name="Tekstas", max_length=1000)

    class Meta:
        verbose_name = 'Komentaras'
        verbose_name_plural = 'Komentarai'
        ordering = ['-date_created']


class Profilis(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profilis')
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
