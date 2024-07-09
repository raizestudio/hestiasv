from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Model for storing users"""

    avatar = models.ImageField(_("Avatar"), upload_to="users/avatars/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    phone_numbers = models.ManyToManyField("geosys.PhoneNumber", related_name="user_phone_numbers", blank=True)
    addresses = models.ManyToManyField("geosys.Address", related_name="user_addresses", blank=True)
    role = models.ForeignKey("user.Role", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email

    def set_email(self, email):
        self.email = email
        self.save()

    def set_first_name(self, first_name):
        self.first_name = first_name
        self.save()

    def set_last_name(self, last_name):
        self.last_name = last_name
        self.save()


class UserPreferences(models.Model):
    """Model for storing user preferences"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(_("Langue"), max_length=255)
    theme = models.CharField(_("Thème"), max_length=255)

    class Meta:
        verbose_name = _("Préférence utilisateur")
        verbose_name_plural = _("Préférences utilisateurs")

    def __str__(self):
        return self.user.username


class UserSecurity(models.Model):
    """Model for storing user security"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(_("Email vérifié"), default=False)
    is_phone_verified = models.BooleanField(_("Téléphone vérifié"), default=False)
    is_two_factor_enabled = models.BooleanField(_("Double authentification activée"), default=False)
    anti_phishing_code = models.CharField(_("Code anti-phishing"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Sécurité utilisateur")
        verbose_name_plural = _("Sécurités utilisateurs")

    def __str__(self):
        return self.user.username


class Group(models.Model):
    """Model for storing user groups"""

    code = models.CharField(_("Code"), max_length=255, primary_key=True)
    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))
    color = models.CharField(_("Couleur"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)

    class Meta:
        verbose_name = _("Groupe utilisateur")
        verbose_name_plural = _("Groupes utilisateurs")

    def __str__(self):
        return self.name


class Role(models.Model):
    """Model for storing roles"""

    code = models.CharField(_("Code"), max_length=255, primary_key=True)
    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))
    slug = models.SlugField(_("Slug"))

    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _("Rôle")
        verbose_name_plural = _("Rôles")

    def __str__(self):
        return self.name
