from rest_framework import viewsets, status
from rest_framework.response import Response

from place.models import Place
from place.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer