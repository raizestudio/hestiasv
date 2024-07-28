from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from geosys.serializers import AddressSerializer, PhoneNumberSerializer
from user.models import Group, Role, User, UserPreferences, UserSecurity


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = "__all__"
        read_only_fields = ["id"]


class UserSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSecurity
        fields = "__all__"
        read_only_fields = ["id"]


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class RoleSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        expandable_fields = {
            "group": GroupSerializer,
        }


class UserSerializer(FlexFieldsModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = User
        exclude = ["password"]
        expandable_fields = {
            "role": RoleSerializer,
            "addresses": (AddressSerializer, {"many": True}),
            "phone_numbers": (PhoneNumberSerializer, {"many": True}),
            "user_preferences": UserPreferencesSerializer,
            "user_security": UserSecuritySerializer,
        }

        read_only_fields = ["id", "date_joined"]
