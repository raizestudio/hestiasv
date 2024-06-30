from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Menu, MenuItem
from core.serializers import MenuItemSerializer, MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="user-menu")
    def user_menu(self, request, *args, **kwargs):
        response = []
        _menus = Menu.objects.all()
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
