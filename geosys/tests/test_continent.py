import pytest

from geosys.models import Continent

from .factories.factory_continent import ContinentFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestContinents:
    def test_continent_creation(self):
        """Test continent creation"""
        continent = ContinentFactory()
        assert Continent.objects.filter(code=continent.code).exists()

    def test_continent_update(self):
        """Test continent update"""
        continent = ContinentFactory()
        continent.code = "XX"
        continent.save()

        assert Continent.objects.filter(code="XX").exists()

    def test_continent_deletion(self):
        """Test continent deletion"""
        continent = ContinentFactory()
        continent.code = "ZZ"
        continent.save()

        assert Continent.objects.filter(code="ZZ").exists()

        continent.delete()
        assert not Continent.objects.filter(code="ZZ").exists()
