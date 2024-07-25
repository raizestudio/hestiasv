from rest_access_policy import AccessViewSetMixin
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from asset.models import Asset
from asset.policies import AssetAccessPolicy
from asset.serializers import AssetSerializer
from core.paginations import DefaultPageNumberPagination


class AssetViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    access_policy = AssetAccessPolicy
    pagination_class = DefaultPageNumberPagination

    def get_serializer_context(self):
        """Extra context provided to the serializer class."""
        context = super(AssetViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def list(self, request, *args, **kwargs):
        objects_param = request.query_params.get("objects", None)
        if objects_param == "all":
            queryset = Asset.objects.all_objects()
        elif objects_param == "deleted":
            queryset = Asset.objects.deleted_objects()
        else:
            queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        objects_param = request.query_params.get("objects", None)
        if objects_param == "all":
            instance = Asset.objects.all_objects().get(pk=kwargs.get("pk"))
        elif objects_param == "deleted":
            instance = Asset.objects.deleted_objects().get(pk=kwargs.get("pk"))
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
        restore = request.GET.get("restore") in ["true", "True"]
        instance = Asset.objects.all_objects().get(pk=kwargs.get("pk"))
        if restore and instance.deleted_at is not None:
            instance.restore(strict=False)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
