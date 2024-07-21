from django.db import models
from django.utils.translation import gettext_lazy as _


class History(models.Model):
    """Abstract model for storing history related information"""

    created_at = models.DateTimeField(_("Créé à"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour à"), auto_now=True)
    created_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="created")
    updated_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="updated")

    class Meta:
        abstract = True
        verbose_name = _("Historique")
        verbose_name_plural = _("Historiques")
