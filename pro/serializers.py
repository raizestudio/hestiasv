from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from pro.models import Enterprise, EnterpriseMember, GroupPro, SelfEmployed
from user.serializers import UserSerializer


class GroupProSerializer(serializers.ModelSerializer):
    """Serializer for GroupPro model"""

    class Meta:
        model = GroupPro
        fields = "__all__"


class EnterpriseSerializer(FlexFieldsModelSerializer):
    """Serializer for Enterprise model"""

    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Enterprise
        fields = [
            "id",
            "name",
            "legal_status",
            "siret",
            "siren",
            "is_active",
            "creation_date",
            "slug",
            "created_at",
            "updated_at",
            "author",
            "updated_by",
            "group_pro",
            "members_count",
        ]
        expandable_fields = {
            "author": UserSerializer,
            "updated_by": UserSerializer,
            "group_pro": GroupProSerializer,
        }
        read_only_fields = ["created_at", "author"]

    def create(self, validated_data):
        """Create a new Quotation instance and assign the current user as the author"""
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super(EnterpriseSerializer, self).create(validated_data)

    def get_members_count(self, obj):
        """Method for getting members count"""

        return obj.members.count()


class SelfEmployedSerializer(serializers.ModelSerializer):
    """Serializer for SelfEmployed model"""

    class Meta:
        model = SelfEmployed
        fields = "__all__"


class EnterpriseMemberSerializer(serializers.ModelSerializer):
    """Serializer for EnterpriseMember model"""

    class Meta:
        model = EnterpriseMember
        fields = "__all__"
