import pytest

from user.models import Group
from user.tests.factories.factory_group import GroupFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_group_creation(self):
        """Test group creation"""
        group = GroupFactory()
        assert Group.objects.filter(code=group.code).exists()
