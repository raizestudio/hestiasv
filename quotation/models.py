from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from place.models import Place
from service.models import Service


class Quotation(models.Model):

    label = models.CharField(max_length=255)
    description = models.TextField()
    quotation_references = models.ManyToManyField("QuotationReference", verbose_name=_("Quotation References"))

    class Meta:
        verbose_name = _("Quotation")
        verbose_name_plural = _("Quotations")

    def __str__(self):
        return self.label


class QuotationReference(models.Model):

    label = models.CharField(max_length=255)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    to_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    to_object_id = models.PositiveIntegerField(null=True)
    to = GenericForeignKey("to_content_type", "to_object_id")  # 'to' which geographical location this quotation is for

    class Meta:
        verbose_name = _("Quotation Reference")
        verbose_name_plural = _("Quotation References")

    def __str__(self):
        return self.label
