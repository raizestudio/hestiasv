from rest_access_policy import AccessViewSetMixin
from rest_framework import status, viewsets
from rest_framework.response import Response

from core.paginations import DefaultPageNumberPagination
from service.models import Service
from service.policies import ServiceAccessPolicy
from service.serializers import ServiceSerializer


class ServiceViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    access_policy = ServiceAccessPolicy
    pagination_class = DefaultPageNumberPagination
