from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from core.serializers import CategorySerializer, TagSerializer
from service.models import Service
from user.serializers import UserSerializer


class ServiceSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"
        expandable_fields = {
            "created_by": UserSerializer,
            "updated_by": UserSerializer,
            "tags": (TagSerializer, {"many": True}),
            "categories": (CategorySerializer, {"many": True}),
        }
        read_only_fields = ["created_at", "created_by"]
