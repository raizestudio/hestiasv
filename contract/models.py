from django.db import models

from core.models import SoftDelete
from history.models import History
from quotation.models import Quotation


class Contract(History, SoftDelete):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    quotation_reference = models.OneToOneField(Quotation, on_delete=models.CASCADE, related_name="contract_quotation_reference", null=True, blank=True)

    author = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="contract_author", null=True, blank=True)
    updated_by = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="contract_maintainer", null=True, blank=True)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.id
