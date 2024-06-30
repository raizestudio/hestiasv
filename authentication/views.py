from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.models import Token
from authentication.serializers import TokenSerializer
from user.models import User


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

        _token = Token.generate_token()
        data = {"token": _token, "user": _user.id}
        serializer = TokenSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
