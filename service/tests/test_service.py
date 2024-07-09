import pytest

from service.models import Service
from service.tests.factories.factory_service import ServiceFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_service_creation(self):
        """Test service creation"""
        service = ServiceFactory()
        assert Service.objects.filter(name=service.name).exists()

    def test_service_update(self):
        """Test service update"""
        service = ServiceFactory()
        new_name = "New name"
        service.name = new_name
        service.save()
        assert Service.objects.filter(name=new_name).exists()
