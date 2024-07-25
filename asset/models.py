from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Category, SoftDelete, Tag
from history.models import History


class Asset(History, SoftDelete):
    """Model for storing assets"""

    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    slug = models.SlugField(_("Slug"), unique=True)

    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), blank=True, related_name="asset_tags")
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"), blank=True, related_name="asset_categories")

    author = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="asset_author", null=True, blank=True)
    updated_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="asset_updated", null=True, blank=True)

    class Meta:
        verbose_name = _("Actif")
        verbose_name_plural = _("Actifs")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
