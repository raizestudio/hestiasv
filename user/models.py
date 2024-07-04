from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Model for storing users"""

    avatar = models.ImageField(_("Avatar"), upload_to="users/avatars/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    adress = models.ForeignKey("geosys.Adress", on_delete=models.CASCADE, blank=True, null=True)
    groups = models.ManyToManyField("user.Group", related_name="user_groups", blank=True)

    def __str__(self):
        return self.email

    def set_email(self, email):
        self.email = email
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

    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("Groupe utilisateur")
        verbose_name_plural = _("Groupes utilisateurs")

    def __str__(self):
        return self.name


class Role(models.Model):
    """Model for storing roles"""

    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Rôle")
        verbose_name_plural = _("Rôles")

    def __str__(self):
        return self.name
