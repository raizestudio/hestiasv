from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from core.paginations import DefaultPageNumberPagination
from service.models import Service
from service.policies import ServiceAccessPolicy
from service.serializers import ServiceSerializer


class ServiceViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    """ViewSet for Service model"""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    access_policy = ServiceAccessPolicy
    pagination_class = DefaultPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ["name"]
    ordering_fields = ["id", "created_at", "updated_at", "name", "description", "author", "updated_by"]
    search_fields = ["name"]

    def get_serializer_context(self):
        """Extra context provided to the serializer class."""
        context = super(ServiceViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        objects_param = request.query_params.get("objects", None)
        if objects_param == "all":
            queryset = Service.objects.all_objects()
        elif objects_param == "deleted":
            queryset = Service.objects.deleted_objects()
        else:
            queryset = self.get_queryset()

        # filters
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        objects_param = request.query_params.get("objects", None)
        if objects_param == "all":
            instance = Service.objects.all_objects().get(pk=kwargs.get("pk"))
        elif objects_param == "deleted":
            instance = Service.objects.deleted_objects().get(pk=kwargs.get("pk"))
        else:
            instance = self.get_object()

        # instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = Service.objects.all_objects().get(pk=kwargs.get("pk"))
        if instance.deleted_at is not None:
            instance.restore(strict=False)
            return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
