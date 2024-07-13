from rest_framework import serializers

from pro.models import Enterprise, GroupPro, SelfEmployed


class GroupProSerializer(serializers.ModelSerializer):
    """Serializer for GroupPro model"""

    class Meta:
        model = GroupPro
        fields = "__all__"


class EnterpriseSerializer(serializers.ModelSerializer):
    """Serializer for Enterprise model"""

    class Meta:
        model = Enterprise
        fields = "__all__"


class SelfEmployedSerializer(serializers.ModelSerializer):
    """Serializer for SelfEmployed model"""

    class Meta:
        model = SelfEmployed
        fields = "__all__"
