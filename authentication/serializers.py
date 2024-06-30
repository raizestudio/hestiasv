from rest_framework import serializers

from authentication.models import Refresh, Session, Token


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = "__all__"


class RefreshSerializer(serializers.ModelSerializer):

    class Meta:
        model = Refresh
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = "__all__"
