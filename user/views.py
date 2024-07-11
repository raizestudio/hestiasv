from django.shortcuts import render
from rest_access_policy import AccessViewSetMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.paginations import DefaultPageNumberPagination
from pro.models import Enterprise, SelfEmployed
from user.models import Group, Role, User, UserPreferences, UserSecurity
from user.policies import BaseUserAccessPolicy
from user.serializers import (
    GroupSerializer,
    RoleSerializer,
    UserPreferencesSerializer,
    UserSecuritySerializer,
    UserSerializer,
)


class UserViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    access_policy = BaseUserAccessPolicy
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    pagination_class = DefaultPageNumberPagination

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="retrieve-dashboard", url_name="retrieve_dashboard")
    def retrieve_dashboard(self, request, *args, **kwargs) -> Response:
        user = request.user

        if user.is_anonymous:
            return Response(
                {"detail": "You must be logged in to access this resource"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        dashboard = {"new_users": User.objects.all().count(), "new_enterprises": Enterprise.objects.all().count(), "new_pros": SelfEmployed.objects.all().count()}

        if user.role.group.code == "GR-ADM":
            return Response(dashboard, status=status.HTTP_200_OK)

        return Response({"detail": "No dashboard for you."}, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs) -> Response:
        roles = self.serializer_class(self.queryset, many=True).data
        return Response(roles, status=status.HTTP_200_OK)
