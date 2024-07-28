from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class History(models.Model):
    """Abstract model for storing history related information"""

    created_at = models.DateTimeField(_("Créé à"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour à"), auto_now=True)
    author = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="author",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="updated",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        verbose_name = _("Historique")
        verbose_name_plural = _("Historiques")


class TimelineAction(models.Model):
    """Model for storing timeline actions"""

    name = models.CharField(_("Nom"), max_length=255)

    class Meta:
        verbose_name = _("Action de la chronologie")
        verbose_name_plural = _("Actions de la chronologie")


class Timeline(models.Model):
    """Abstract model for storing timeline related information"""

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="timelines")
    action = models.ForeignKey(TimelineAction, on_delete=models.CASCADE, related_name="timelines")
    timestamp = models.DateTimeField(_("Horodatage"), auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey("content_type", "target_id")

    class Meta:
        verbose_name = _("Chronologie")
        verbose_name_plural = _("Chronologies")
        indexes = [models.Index(fields=["content_type", "target_id"])]
        ordering = ["-timestamp"]
        get_latest_by = "timestamp"
