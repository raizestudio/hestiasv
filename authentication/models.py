import base64
import os
import uuid

import jwt
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class Token(models.Model):
    """Model for storing tokens"""

    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def __str__(self):
        return self.token

    @staticmethod
    def generate_token(user: User) -> str:
        return jwt.encode({"user": user}, str(os.urandom(24)), algorithm="HS256")  # FIXME: Change secret to a more secure value


class Refresh(models.Model):
    """Model for storing refresh tokens"""

    refresh = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Refresh"
        verbose_name_plural = "Refreshes"

    def __str__(self):
        return self.refresh

    @staticmethod
    def generate_refresh() -> str:
        random_bytes = os.urandom(24)
        base64_bytes = base64.b64encode(random_bytes)
        return base64_bytes.decode("utf-8")


class Session(models.Model):
    """Model for storing sessions"""

    session = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE, null=True)
    refresh = models.ForeignKey(Refresh, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        return self.session

    @staticmethod
    def generate_session() -> str:
        return str(uuid.uuid4())


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
