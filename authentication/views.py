from django.db import transaction
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.models import Refresh, Session, Token
from authentication.serializers import (
    RefreshSerializer,
    SessionSerializer,
    TokenSerializer,
)
from user.models import User
from user.serializers import UserSerializer


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     token = Token.generate_token()
    #     data["tk"] = token
    #     serializer = TokenSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=["post"])
    # def authenticate(self, request, *args, **kwargs):
    #     data = request.data.copy()

    #     if "username" not in data:
    #         return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    #     if "password" not in data:
    #         return Response({"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

    #     username = data.get("username")
    #     password = data.get("password")

    #     _user = User.objects.filter(username=username).first()

    #     if not _user:
    #         return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    #     if not _user.check_password(password):
    #         return Response({"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

    #     _token = Token.generate_token()
    #     data = {"token": _token, "user": _user.id}
    #     serializer = TokenSerializer(data=data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="session-id", url_name="session_id")
    def get_session_id(self, request, *args, **kwargs):
        _session = Session.generate_session()
        return Response({"session": _session}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def authenticate(self, request, *args, **kwargs):
        data = request.data.copy()

        if "username" not in data:
            return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        if "password" not in data:
            return Response({"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        username = data.get("username")
        password = data.get("password")

        _user = User.objects.filter(username=username).first()

        if not _user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not _user.check_password(password):
            return Response({"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        _token = Token.generate_token(user=_user.id)

        if Token.objects.filter(user=_user).exists():  # TODO: just for testing, in prod the token should be blacklisted and deleted later
            Token.objects.filter(user=_user).delete()
            Refresh.objects.filter(user=_user).delete()

        data = {"token": _token, "user": _user.id}
        token = TokenSerializer(data=data)

        _refresh = Refresh.generate_refresh()
        data = {"refresh": _refresh, "user": _user.id}
        refresh = RefreshSerializer(data=data)

        with transaction.atomic():
            if all([token.is_valid(), refresh.is_valid()]):
                token.save()
                refresh.save()

                _token = Token.objects.get(token=_token)
                _refresh = Refresh.objects.get(refresh=_refresh)
            else:
                return Response([token.errors, refresh.errors], status=status.HTTP_400_BAD_REQUEST)

            _session = Session.generate_session()
            data = {"session": _session, "user": _user.id, "token": _token.id, "refresh": _refresh.id}
            session = SessionSerializer(data=data)

            if session.is_valid():
                session.save()
                data = session.data.copy()
                data["token"] = _token.token
                data["refresh"] = _refresh.refresh
                data["user"] = UserSerializer(_user).data
                return Response(data, status=status.HTTP_201_CREATED)

        return Response([token.errors, refresh.errors, session.errors], status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="retrieve-from-token")
    def retrieve_from_token(self, request, *args, **kwargs):
        token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return Response({"message": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        _token = Token.objects.filter(token=token).first()

        if not _token:
            return Response({"message": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

        _session = Session.objects.filter(token=_token).first()
        if not _session:
            return Response({"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {"session": _session.session, "user": _session.user, "token": _token.token, "refresh": _session.refresh.refresh}

        data["token"] = _token.token
        data["refresh"] = _session.refresh.refresh
        data["user"] = UserSerializer(_session.user).data
        return Response(data, status=status.HTTP_200_OK)
