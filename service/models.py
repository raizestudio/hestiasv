from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Category, SoftDelete, Tag
from history.models import History


class ServiceManager(models.Manager):
    """Manager for Service model"""

    # TODO: Implement custom methods for ServiceManager
    pass


class ServiceQuerySet(models.QuerySet):
    """QuerySet for Service model"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self = self.select_related("author", "updated_by").prefetch_related("tags", "categories")


class Service(History, SoftDelete):
    """Model for storing services"""

    name = models.CharField(_("Nom"), max_length=255, unique=True)
    description = models.TextField(_("Description"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    estimated_duration = models.CharField(_("Estimated Duration"), max_length=255, blank=True)  # TODO: Change to DurationField maybe? Not supported by SQLite ( afaiu )
    slug = models.SlugField(_("Slug"), unique=True)

    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"), blank=True, related_name="service_tags")
    categories = models.ManyToManyField(
        Category,
        verbose_name=_("Categories"),
        blank=True,
        related_name="service_categories",
    )

    author = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="service_author",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="service_maintainer",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
