from rest_access_policy import AccessViewSetMixin
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import AppSetting, Menu, MenuItem
from core.policies import MenuAccessPolicy
from core.serializers import AppSettingSerializer, MenuItemSerializer, MenuSerializer


class MenuViewSet(AccessViewSetMixin, viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    access_policy = MenuAccessPolicy

    def get_queryset(self):
        return self.access_policy.scope_queryset(self.request, Menu.objects.all())

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="user-menu")
    def user_menu(self, request, *args, **kwargs):
        response = []
        print(f"DEBUG: {self.queryset.filter(groups=request.user.role.group.code)}")
        # print(f"DEBUG: {self.queryset.groups.filter(code=request.user.role.group.code)}")
        _menus = self.queryset.filter(groups=request.user.role.group.code)
        menus = MenuSerializer(_menus, many=True)
        for _menu in _menus:
            menu = MenuSerializer(_menu)
            _menu_items = MenuItem.objects.filter(menu=_menu)
            menu_items = MenuItemSerializer(_menu_items, many=True)
            temp = menu.data.copy()
            temp["menu_items"] = menu_items.data
            response.append(temp)
        # _menu_items = MenuItem.objects.all()
        # menu_items = MenuItemSerializer(_menu_items, many=True)

        return Response(response, status=status.HTTP_200_OK)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AppSettingViewSet(viewsets.ModelViewSet):
    queryset = AppSetting.objects.all()
    serializer_class = AppSettingSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


