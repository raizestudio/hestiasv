from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    """Model for storing services"""

    name = models.CharField(_("Nom"), max_length=255, unique=True)
    description = models.TextField(_("Description"))
    slug = models.SlugField(_("Slug"), unique=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.name