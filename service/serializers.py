from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from core.serializers import CategorySerializer, TagSerializer
from service.models import Service
from user.serializers import UserSerializer


class ServiceSerializer(FlexFieldsModelSerializer):
    """Serializer for Service model"""

    class Meta:
        model = Service
        fields = "__all__"
        expandable_fields = {
            "author": UserSerializer,
            "updated_by": UserSerializer,
            "tags": (TagSerializer, {"many": True}),
            "categories": (CategorySerializer, {"many": True}),
        }
        read_only_fields = ["created_at", "author"]

    def create(self, validated_data):
        """Create a new Service instance and assign the current user as the author"""
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super(ServiceSerializer, self).create(validated_data)
