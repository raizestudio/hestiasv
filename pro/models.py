from django.db import models
from django.utils.translation import gettext_lazy as _


class Pro(models.Model):
    """Model for storing base pro"""

    name = models.CharField(_("Nom"), max_length=255)
    legal_status = models.CharField(_("Statut légal"), max_length=255)
    siret = models.CharField(_("SIRET"), max_length=255)
    siren = models.CharField(_("SIREN"), max_length=255)
    creation_date = models.DateField(_("Date de création"))
    slug = models.SlugField(_("Slug"), max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class GroupPro(models.Model):
    """Model for storing group pro"""

    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("Groupe pro")
        verbose_name_plural = _("Groupes pro")

    def __str__(self):
        return self.name


class Entreprise(Pro, models.Model):
    """Model for storing agencies"""

    email = models.EmailField(_("Email"))

    group_pro = models.ForeignKey("pro.GroupPro", verbose_name=_("Groupe pro"), on_delete=models.CASCADE)
    phone_numbers = models.ManyToManyField("geosys.PhoneNumber", verbose_name=_("Numéros de téléphone"))

    class Meta:
        verbose_name = _("Agence")
        verbose_name_plural = _("Agences")

    def __str__(self):
        return self.name


class SelfEmployed(Pro, models.Model):
    """Model for storing self-employed"""

    class Meta:
        verbose_name = _("Indépendant")
        verbose_name_plural = _("Indépendants")

    def __str__(self):
        return self.name
