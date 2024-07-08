from rest_framework import serializers

from geosys.models import (
    Address,
    City,
    CityType,
    Continent,
    Country,
    Department,
    Region,
    Street,
    StreetLabel,
)


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""

    class Meta:
        model = Address
        fields = "__all__"


class ContinentSerializer(serializers.ModelSerializer):
    """Serializer for Continent model"""

    class Meta:
        model = Continent
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model"""

    class Meta:
        model = Country
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for Region model"""

    class Meta:
        model = Region
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""

    class Meta:
        model = Department
        fields = "__all__"


class CityTypeSerializer(serializers.ModelSerializer):
    """Serializer for CityType model"""

    class Meta:
        model = CityType
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model"""

    class Meta:
        model = City
        fields = "__all__"


class StreetLabelSerializer(serializers.ModelSerializer):
    """Serializer for StreetLabel model"""

    class Meta:
        model = StreetLabel
        fields = "__all__"


class StreetSerializer(serializers.ModelSerializer):
    """Serializer for Street model"""

    class Meta:
        model = Street
        fields = "__all__"
