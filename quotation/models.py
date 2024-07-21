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


class QuotationReferenceScope(models.Model):

    continent = models.ManyToManyField(
        "geosys.Continent",
    )
    country = models.ManyToManyField(
        "geosys.Country",
    )
    department = models.ManyToManyField(
        "geosys.Department",
    )
    city = models.ManyToManyField(
        "geosys.City",
    )

    agency = models.ManyToManyField(
        "pro.Enterprise",
    )

    self_employed = models.ManyToManyField(
        "pro.SelfEmployed",
    )


class QuotationReference(models.Model):

    label = models.CharField(max_length=255)
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)

    quotation_reference_scope = models.ForeignKey(QuotationReferenceScope, on_delete=models.CASCADE, null=True, related_name="scope")

    class Meta:
        verbose_name = _("Quotation Reference")
        verbose_name_plural = _("Quotation References")

    def __str__(self):
        return self.label
