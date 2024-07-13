from rest_access_policy import AccessViewSetMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from pro.models import Enterprise, SelfEmployed
from pro.policies import EnterpriseAccessPolicy
from pro.serializers import EnterpriseSerializer, SelfEmployedSerializer
from user.models import User


class EnterpriseViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    access_policy = EnterpriseAccessPolicy

    @action(methods=["post"], detail=True, url_path="add-user", url_name="add_user")
    def add_user(self, request, pk=None, *args, **kwargs):
        user = request.data.get("user")
        position = request.data.get("position")

        _user = User.objects.get(pk=user)
        _enterprise = self.get_object()
        _enterprise.add_user(_user, position)
        _enterprise.save()

        enterprise = self.get_serializer(_enterprise)
        return Response(data=enterprise.data, status=status.HTTP_200_OK)


class SelfEmployedViewSet(viewsets.ModelViewSet):
    queryset = SelfEmployed.objects.all()
    serializer_class = SelfEmployedSerializer
