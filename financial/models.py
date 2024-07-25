from django.db import models
from django.utils.translation import gettext_lazy as _

from geosys.models import Currency


class Price(models.Model):
    """Model for storing prices"""

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    taxe_excluded = models.BooleanField(default=False)

    class Meta:
        abstract = True
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")

    def __str__(self):
        return self.amount
