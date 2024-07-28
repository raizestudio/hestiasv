import random
import string

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import SoftDelete, SoftDeleteManager


class CUserManager(UserManager, SoftDeleteManager):
    """Manager for User model"""

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db).filter(role_id__isnull=False)

    def all_objects(self):
        return UserQuerySet(self.model, using=self._db)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserQuerySet(models.QuerySet):
    """QuerySet for User model"""

    def active(self):
        return self.filter(is_active=True)


class User(AbstractUser, SoftDelete):
    """Model for storing users"""

    avatar = models.ImageField(_("Avatar"), upload_to="users/avatars/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    phone_numbers = models.ManyToManyField("geosys.PhoneNumber", related_name="user_phone_numbers", blank=True)
    addresses = models.ManyToManyField("geosys.Address", related_name="user_addresses", blank=True)
    role = models.ForeignKey("user.Role", on_delete=models.CASCADE, null=True)

    user_preferences = models.OneToOneField("user.UserPreferences", on_delete=models.CASCADE, null=True)
    user_security = models.OneToOneField("user.UserSecurity", on_delete=models.CASCADE, null=True)

    objects = CUserManager()

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ["-date_joined"]

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

    def set_role(self, role):
        self.role = role
        self.save()

    def set_address(self, address):
        self.addresses.add(address)
        self.save()

    def set_user_preferences(self, user_preferences):
        self.user_preferences = user_preferences
        self.save()

    def set_user_security(self, user_security):
        self.user_security = user_security
        self.save()

    @staticmethod
    def generate_temporary_username():
        return "guest_" + "".join(random.choices(string.ascii_letters + string.digits, k=6))


class UserPreferences(models.Model):
    """Model for storing user preferences"""

    language = models.CharField(_("Langue"), max_length=255)
    theme = models.CharField(_("Thème"), max_length=255)
    is_public_profile = models.BooleanField(_("Profil public"), default=True)

    class Meta:
        verbose_name = _("Préférence utilisateur")
        verbose_name_plural = _("Préférences utilisateurs")

    def __str__(self):
        return self.user.username


class UserSecurity(models.Model):
    """Model for storing user security"""

    email_validation_code = models.CharField(_("Code de validation email"), max_length=255, blank=True, unique=True)
    email_validation_code_expires_at = models.DateTimeField(
        _("Code de validation email expire à"),
        default=timezone.now() + timezone.timedelta(minutes=30),
    )
    email_validation_code_sent_at = models.DateTimeField(_("Code de validation email envoyé à"))
    email_validation_code_confirmed_at = models.DateTimeField(_("Code de validation email expire à"), blank=True, null=True)
    is_phone_verified = models.BooleanField(_("Téléphone vérifié"), default=False)
    is_two_factor_enabled = models.BooleanField(_("Double authentification activée"), default=False)
    anti_phishing_code = models.CharField(_("Code anti-phishing"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Sécurité utilisateur")
        verbose_name_plural = _("Sécurités utilisateurs")

    def __str__(self):
        return self.user.username

    @staticmethod
    def generate_email_validation_code():
        code = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        return code


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
