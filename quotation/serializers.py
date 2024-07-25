from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from asset.serializers import AssetSerializer
from geosys.serializers import CurrencySerializer
from quotation.models import Quotation, QuotationReference, QuotationReferenceScope
from service.serializers import ServiceSerializer
from user.serializers import UserSerializer


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = "__all__"


class QuotationReferenceScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationReferenceScope
        fields = "__all__"


class QuotationReferenceSerializer(FlexFieldsModelSerializer):
    """Serializer for QuotationReference model"""

    class Meta:
        model = QuotationReference
        fields = "__all__"
        expandable_fields = {
            "service": ServiceSerializer,
            "asset": AssetSerializer,
            "currency": CurrencySerializer,
            "quotation_reference_scope": QuotationReferenceScopeSerializer,
            "author": UserSerializer,
            "updated_by": UserSerializer,
        }
        read_only_fields = ["created_at", "author"]

    def create(self, validated_data):
        """Create a new QuotationReference instance and assign the current user as the author"""
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super(ServiceSerializer, self).create(validated_data)
