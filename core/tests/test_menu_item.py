import pytest

from core.models import MenuItem
from core.tests.factories.factory_menu import MenuFactory
from core.tests.factories.factory_menu_item import MenuItemFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_menu_item_creation(self):
        """Test menu item creation"""
        menu_item = MenuItemFactory()
        assert MenuItem.objects.filter(name=menu_item.name).exists()
