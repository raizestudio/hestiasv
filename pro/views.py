from rest_access_policy import AccessViewSetMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.paginations import DefaultPageNumberPagination
from pro.models import Enterprise, EnterpriseMember, SelfEmployed
from pro.policies import EnterpriseAccessPolicy
from pro.serializers import (
    EnterpriseMemberSerializer,
    EnterpriseSerializer,
    SelfEmployedSerializer,
)
from user.models import User


class EnterpriseViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    access_policy = EnterpriseAccessPolicy
    pagination_class = DefaultPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, url_path="add-user", url_name="add_user")
    def add_user(self, request, pk=None, *args, **kwargs):
        # FIXME: Users aren't assigned through a m2m field, but through a separate model EnterpriseMember
        user = request.data.get("user")
        position = request.data.get("position")

        _user = User.objects.get(pk=user)
        _enterprise = self.get_object()
        _enterprise.add_user(_user, position)
        _enterprise.save()

        enterprise = self.get_serializer(_enterprise)
        return Response(data=enterprise.data, status=status.HTTP_200_OK)


class EnterpriseMemberViewSet(viewsets.ModelViewSet):
    queryset = EnterpriseMember.objects.all()
    serializer_class = EnterpriseMemberSerializer
    access_policy = EnterpriseAccessPolicy
    pagination_class = DefaultPageNumberPagination


class SelfEmployedViewSet(viewsets.ModelViewSet):
    queryset = SelfEmployed.objects.all()
    serializer_class = SelfEmployedSerializer
    access_policy = EnterpriseAccessPolicy
    pagination_class = DefaultPageNumberPagination
