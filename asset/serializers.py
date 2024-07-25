from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from asset.models import Asset
from core.serializers import CategorySerializer, TagSerializer
from user.serializers import UserSerializer


class AssetSerializer(FlexFieldsModelSerializer):
    """Serializer for Asset model"""

    class Meta:
        model = Asset
        fields = "__all__"
        expandable_fields = {
            "author": UserSerializer,
            "updated_by": UserSerializer,
            "tags": (TagSerializer, {"many": True}),
            "categories": (CategorySerializer, {"many": True}),
        }

    def create(self, validated_data):
        """Create a new Asset instance and assign the current user as the author"""
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super(AssetSerializer, self).create(validated_data)
