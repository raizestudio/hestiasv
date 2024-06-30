from rest_framework import serializers

from authentication.models import Token


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = "__all__"
