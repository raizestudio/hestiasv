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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)

    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    addresses = AddressSerializer(read_only=True, many=True)

    class Meta:
        model = User
        exclude = ["password"]
