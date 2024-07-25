import pytest

from asset.models import Asset
from asset.tests.factories.factory_asset import AssetFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_service_creation(self):
        """Test asset creation"""
        asset = AssetFactory()
        assert Asset.objects.filter(name=asset.name).exists()

    def test_service_update(self):
        """Test asset update"""
        asset = AssetFactory()
        new_name = "New name"
        asset.name = new_name
        asset.save()
        assert Asset.objects.filter(name=new_name).exists()
