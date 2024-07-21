from rest_framework import serializers

from pro.models import Enterprise, EnterpriseMember, GroupPro, SelfEmployed


class GroupProSerializer(serializers.ModelSerializer):
    """Serializer for GroupPro model"""

    class Meta:
        model = GroupPro
        fields = "__all__"


class EnterpriseSerializer(serializers.ModelSerializer):
    """Serializer for Enterprise model"""

    members_count = serializers.SerializerMethodField()
    group_pro = GroupProSerializer()

    class Meta:
        model = Enterprise
        fields = ["id", "name", "legal_status", "siret", "siren", "is_active", "creation_date", "slug", "created_at", "updated_at", "group_pro", "members_count"]

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
