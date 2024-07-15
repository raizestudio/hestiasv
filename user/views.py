from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import timezone
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

    @action(detail=False, methods=["get"], url_path="search", url_name="search")
    def list_w_term(self, request, *args, **kwargs) -> Response:
        field = request.query_params.get("field")
        term = request.query_params.get("term")

        if not field:
            return Response({"detail": "Field is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not term:
            return Response({"detail": "Term is required"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"DEBUG field: {field} - term: {term}")

        users = User.objects.filter(username__icontains=term)
        print(f"DEBUG users: {users}")
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="email/activate/(?P<email_code>[^/.]+)", url_name="email_activate")
    def confirm_email(self, request, email_code: str, *args, **kwargs) -> Response:
        if not email_code:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            _user_security = UserSecurity.objects.get(email_validation_code=email_code)

        except UserSecurity.DoesNotExist:
            return Response({"detail": "The code does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if _user_security.email_validation_code_expires_at < timezone.now():
            return Response({"detail": "The code has expired"}, status=status.HTTP_400_BAD_REQUEST)

        _user_security.email_validation_code_confirmed_at = timezone.now()
        _user = _user_security.user

        return Response({"detail": "User confirmed", "user": UserSerializer(_user).data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="email", url_name="email")
    def create_from_email(self, request, *args, **kwargs) -> Response:
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        _user = User.objects.create(email=email, is_active=False)
        email_code = UserSecurity.generate_email_validation_code()
        _user_security = UserSecurity.objects.create(user=_user, email_validation_code=email_code, email_validation_code_sent_at=timezone.now())

        # activation_link = request.build_absolute_uri(f"users/email/activate/{email_code}")
        activation_link = f"http://localhost:3000/user/activate/{email_code}"
        send_mail("Votre compte en quelques minutes.", f"Validez votre inscription en cliquant sur le lien suivant: {activation_link} ", "no-reply@hestia.com", [email])
        return Response({"detail": "User created", "user": UserSerializer(_user).data}, status=status.HTTP_201_CREATED)

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
