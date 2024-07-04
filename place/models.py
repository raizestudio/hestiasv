from django.db import models
from django.utils.translation import gettext_lazy as _


class Place(models.Model):
    """Model for storing places"""

    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("Lieu")
        verbose_name_plural = _("Lieux")

    def __str__(self):
        return self.name
