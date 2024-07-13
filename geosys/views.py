from rest_framework import status, viewsets
from rest_framework.response import Response

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
from geosys.serializers import (
    AddressSerializer,
    CitySerializer,
    CityTypeSerializer,
    ContinentSerializer,
    CountrySerializer,
    DepartmentSerializer,
    RegionSerializer,
    StreetLabelSerializer,
    StreetSerializer,
)


class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet for Address model"""

    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ContinentViewSet(viewsets.ModelViewSet):
    """ViewSet for Continent model"""

    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """ViewSet for Country model"""

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class RegionViewSet(viewsets.ModelViewSet):
    """ViewSet for Region model"""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department model"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CityTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for CityType model"""

    queryset = CityType.objects.all()
    serializer_class = CityTypeSerializer


class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for City model"""

    queryset = City.objects.all()
    serializer_class = CitySerializer


class StreetLabelViewSet(viewsets.ModelViewSet):
    """ViewSet for StreetLabel model"""

    queryset = StreetLabel.objects.all()
    serializer_class = StreetLabelSerializer


class StreetViewSet(viewsets.ModelViewSet):
    """ViewSet for Street model"""

    queryset = Street.objects.all()
    serializer_class = StreetSerializer
