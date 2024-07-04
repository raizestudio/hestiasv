import pytest

from user.models import User

from .factories.factory_base_user import UserFactory

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestUsers:

    def test_user_creation(self):
        """Test user creation"""
        user = UserFactory(username="test_user")
        assert User.objects.filter(username=user.username).exists()

    # def test_user_update(self):
    #     """Test user update"""
    #     user = UserFactory(username="test_user")
    #     user.username = "test_user_updated"
    #     user.save()

    #     assert User.objects.filter(username="test_user_updated").exists()

    # def test_user_deletion(self):
    #     """Test user deletion"""
    #     user = UserFactory(username="test_user")
    #     assert User.objects.filter(username=user.username).exists(), "User creation failed"

    #     _user.delete()
    #     assert _user.is_deleted, "User deletion failed"

    # def test_user_restore(self):
    #     """Test user restore"""
    #     user = UserFactory(username="test_user")
    #     _user = User.objects.get(username="test_user")
    #     assert User.objects.filter(username=_user.username).exists(), "User creation failed"

    #     _user.delete()
    #     assert _user.is_deleted, "User deletion failed"

    #     _user.restore(strict=False)
    #     assert _user.is_restored, "User restoration failed"

    # def test_user_hard_delete(self):
    #     """Test user hard delete"""
    #     user = UserFactory(username="test_user")
    #     _user = User.objects.get(username="test_user")
    #     assert User.objects.filter(username=_user.username).exists(), "User creation failed"

    #     _user.hard_delete()
    #     assert _user.is_hard_deleted, "User hard deletion failed"
    #     assert not User.objects.filter(username=_user.username).exists(), "User hard deletion failed"
