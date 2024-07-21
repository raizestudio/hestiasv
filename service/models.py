from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Category, SoftDelete, Tag
from history.models import History


class Service(History, SoftDelete):
    """Model for storing services"""

    name = models.CharField(_("Nom"), max_length=255, unique=True)
    description = models.TextField(_("Description"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    estimated_duration = models.CharField(_("Estimated Duration"), max_length=255, blank=True)  # TODO: Change to DurationField maybe?
    slug = models.SlugField(_("Slug"), unique=True)

    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), blank=True, related_name="tags")
    categories = models.ManyToManyField("core.Category", verbose_name=_("Categories"), blank=True, related_name="categories")

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
