from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Model for storing users"""

    avatar = models.ImageField(_("Avatar"), upload_to="users/avatars/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField("authentication.Group", related_name="user_groups", blank=True)

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
