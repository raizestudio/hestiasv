from rest_framework import serializers

from quotation.models import Quotation, QuotationReference


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = "__all__"


class QuotationReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReference
        fields = "__all__"
