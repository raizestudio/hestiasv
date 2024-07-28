import pytest

from pro.models import Enterprise
from pro.tests.factories.factory_enterprise import EnterpriseFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:
    def test_service_creation(self):
        """Test asset creation"""
        asset = EnterpriseFactory()
        assert Enterprise.objects.filter(name=asset.name).exists()

    def test_service_update(self):
        """Test asset update"""
        asset = EnterpriseFactory()
        new_name = "New name"
        asset.name = new_name
        asset.save()
        assert Enterprise.objects.filter(name=new_name).exists()
