import pytest

from pro.models import Enterprise
from pro.tests.factories.factory_entreprise import EnterpriseFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_service_creation(self):
        """Test place creation"""
        place = EnterpriseFactory()
        assert Enterprise.objects.filter(name=place.name).exists()

    def test_service_update(self):
        """Test place update"""
        place = EnterpriseFactory()
        new_name = "New name"
        place.name = new_name
        place.save()
        assert Enterprise.objects.filter(name=new_name).exists()
