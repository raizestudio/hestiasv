from rest_framework import serializers

from geosys.models import (
    Address,
    AddressType,
    City,
    CityType,
    Continent,
    Country,
    Currency,
    Department,
    Language,
    PhoneNumber,
    PhoneNumberType,
    Region,
    Street,
    StreetLabel,
)


class AddressTypeSerializer(serializers.ModelSerializer):
    """Serializer for AddressType model"""

    class Meta:
        model = AddressType
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

    label = StreetLabelSerializer(read_only=True, many=False)

    class Meta:
        model = Street
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""

    country = CountrySerializer(read_only=True, many=False)
    department = DepartmentSerializer(read_only=True, many=False)
    region = RegionSerializer(read_only=True, many=False)
    city = CitySerializer(read_only=True, many=False)
    street = StreetSerializer(read_only=True, many=False)
    address_type = AddressTypeSerializer(read_only=True)

    class Meta:
        model = Address
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currency model"""

    class Meta:
        model = Currency
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language model"""

    class Meta:
        model = Language
        fields = "__all__"


class PhoneNumberTypeSerializer(serializers.ModelSerializer):
    """Serializer for PhoneNumberType model"""

    class Meta:
        model = PhoneNumberType
        fields = "__all__"


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Serializer for PhoneNumber model"""

    phone_number_type = PhoneNumberTypeSerializer(read_only=True, many=False)

    class Meta:
        model = PhoneNumber
        fields = "__all__"
