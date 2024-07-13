import pytest

from core.models import Menu
from core.tests.factories.factory_menu import MenuFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_menu_creation(self):
        """Test menu item creation"""
        menu = MenuFactory()
        assert Menu.objects.filter(name=menu.name).exists()

    def test_menu_update(self):
        """Test menu update"""
        menu = MenuFactory(name="test_menu")
        menu.name = "test_menu_updated"
        menu.save()

        assert Menu.objects.filter(name="test_menu_updated").exists()

    def test_menu_deletion(self):
        """Test menu deletion"""
        menu = MenuFactory(name="test_menu")
        assert Menu.objects.filter(name=menu.name).exists()

        menu.delete()
        assert not Menu.objects.filter(name=menu.name).exists()
