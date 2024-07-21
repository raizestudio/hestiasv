from rest_access_policy import AccessViewSetMixin
from rest_framework import status, viewsets
from rest_framework.response import Response

from core.paginations import DefaultPageNumberPagination
from place.models import Place
from place.policies import PlaceAccessPolicy
from place.serializers import PlaceSerializer


class PlaceViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    access_policy = PlaceAccessPolicy
    pagination_class = DefaultPageNumberPagination
