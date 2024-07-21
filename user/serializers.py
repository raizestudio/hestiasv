from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from geosys.serializers import AddressSerializer
from user.models import Group, Role, User, UserPreferences, UserSecurity


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = "__all__"
        read_only_fields = ["id", "user"]


class UserSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSecurity
        fields = "__all__"
        read_only_fields = ["id", "user"]


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class RoleSerializer(FlexFieldsModelSerializer):
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(FlexFieldsModelSerializer):
    role = RoleSerializer(read_only=True)
    addresses = AddressSerializer(read_only=True, many=True)

    class Meta:
        model = User
        exclude = ["password"]
        expendable_fields = {"role": RoleSerializer, "addresses": (AddressSerializer, {"many": True})}
