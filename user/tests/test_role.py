import pytest

from user.models import Role
from user.tests.factories.factory_role import RoleFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_group_creation(self):
        """Test group creation"""
        role = RoleFactory()
        assert Role.objects.filter(code=role.code).exists()
