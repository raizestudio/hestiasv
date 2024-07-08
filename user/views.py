from django.shortcuts import render
from rest_access_policy import AccessViewSetMixin
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        roles = self.serializer_class(self.queryset, many=True).data
        return Response(roles, status=status.HTTP_200_OK)
