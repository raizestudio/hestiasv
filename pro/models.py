from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import SoftDelete
from history.models import History


class Pro(History, SoftDelete):
    """Model for storing base pro"""

    name = models.CharField(_("Nom"), max_length=255)
    legal_status = models.CharField(_("Statut légal"), max_length=255)
    siret = models.CharField(_("SIRET"), max_length=255)
    siren = models.CharField(_("SIREN"), max_length=255)
    creation_date = models.DateField(_("Date de création"))
    slug = models.SlugField(_("Slug"), max_length=255)
    is_active = models.BooleanField(_("Actif"), default=True)
    # created_at = models.DateTimeField(_("Crée le"), auto_now_add=True)
    # updated_at = models.DateTimeField(_("Modifié le"), auto_now=True)

    phone_numbers = models.ManyToManyField("geosys.PhoneNumber", verbose_name=_("Numéros de téléphone"))
    emails = models.ManyToManyField("geosys.Email", verbose_name=_("Emails"))

    group_pro = models.ForeignKey("pro.GroupPro", verbose_name=_("Groupe pro"), on_delete=models.CASCADE, null=True)

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


class EnterpriseMember(models.Model):
    """Model for storing enterprise users"""

    user = models.ForeignKey("user.User", verbose_name=_("Utilisateur"), on_delete=models.CASCADE)
    position = models.CharField(_("Rôle"), max_length=255)

    date_joined = models.DateTimeField(_("Date de création"), auto_now_add=True)
    enterprise = models.ForeignKey("pro.Enterprise", verbose_name=_("Agence"), on_delete=models.CASCADE, related_name="members")

    class Meta:
        verbose_name = _("Utilisateur d'agence")
        verbose_name_plural = _("Utilisateurs d'agence")

    def __str__(self):
        return self.user.username


class Enterprise(Pro):
    """Model for storing agencies"""

    group_pro = models.ForeignKey("pro.GroupPro", verbose_name=_("Groupe pro"), on_delete=models.CASCADE, null=True)

    author = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="enterprise_author", null=True, blank=True)
    updated_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="enterprise_maintainer", null=True, blank=True)

    class Meta:
        verbose_name = _("Agence")
        verbose_name_plural = _("Agences")

    def __str__(self):
        return self.name

    def add_user(self, user, position):
        """Method for adding user to agency"""

        _enterprise_member = EnterpriseMember.objects.create(user=user, position=position)
        self.members.add(_enterprise_member)


class SelfEmployed(Pro):
    """Model for storing self-employed"""

    author = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="self_employed_author", null=True, blank=True)
    updated_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="self_employed_maintainer", null=True, blank=True)

    class Meta:
        verbose_name = _("Indépendant")
        verbose_name_plural = _("Indépendants")

    def __str__(self):
        return self.name
