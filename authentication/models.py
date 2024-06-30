import uuid

from django.db import models


class Token(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def __str__(self):
        self.tk

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())
