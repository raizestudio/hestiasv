from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from asset.models import Asset
from core.models import SoftDelete
from financial.models import Price
from history.models import History
from service.models import Service


class Quotation(History, SoftDelete):
    STATE_OPTIONS = [
        ("draft", _("Draft")),
        (
            "awaiting",
            _("Awaiting"),
        ),  # Awaiting agency or self-employed to accept the quotation
        ("halted", _("Halted")),  # Quotation is halted by admin or staff
        ("open", _("Open")),
        ("closed", _("Closed")),
        ("cancelled", _("Cancelled")),
    ]

    label = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    quotation_references = models.ManyToManyField("QuotationReference", verbose_name=_("Quotation References"))

    enterprise_accepted = models.ForeignKey(
        "pro.Enterprise",
        on_delete=models.CASCADE,
        related_name="accepted_quotations",
        null=True,
        blank=True,
    )
    self_employed_accepted = models.ForeignKey(
        "pro.SelfEmployed",
        on_delete=models.CASCADE,
        related_name="accepted_quotations",
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="quotation_author",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="quotation_maintainer",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Quotation")
        verbose_name_plural = _("Quotations")
        ordering = ["-created_at"]

    @cached_property
    def total_price(self):
        return sum([quotation_reference.amount for quotation_reference in self.quotation_references.all()])

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


class QuotationReference(History, Price, SoftDelete):
    label = models.CharField(max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    quotation_reference_scope = models.ForeignKey(
        QuotationReferenceScope,
        on_delete=models.CASCADE,
        null=True,
        related_name="scope",
    )

    author = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="quotation_reference_author",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="quotation_reference_maintainer",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Quotation Reference")
        verbose_name_plural = _("Quotation References")
        ordering = ["-created_at"]

    def __str__(self):
        return self.label
