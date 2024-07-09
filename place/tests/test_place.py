import pytest

from place.models import Place
from place.tests.factories.factory_place import PlaceFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_service_creation(self):
        """Test place creation"""
        place = PlaceFactory()
        assert Place.objects.filter(name=place.name).exists()

    def test_service_update(self):
        """Test place update"""
        place = PlaceFactory()
        new_name = "New name"
        place.name = new_name
        place.save()
        assert Place.objects.filter(name=new_name).exists()
