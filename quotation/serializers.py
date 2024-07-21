from rest_framework import serializers

from place.serializers import PlaceSerializer
from quotation.models import Quotation, QuotationReference, QuotationReferenceScope
from service.serializers import ServiceSerializer


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = "__all__"


class QuotationReferenceScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReferenceScope
        fields = "__all__"


class QuotationReferenceSerializer(serializers.ModelSerializer):

    service = ServiceSerializer()
    place = PlaceSerializer()
    quotation_reference_scope = QuotationReferenceScopeSerializer()

    class Meta:
        model = QuotationReference
        fields = "__all__"
