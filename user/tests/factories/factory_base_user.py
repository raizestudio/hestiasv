import factory
from django.utils import timezone
from faker import Faker

from user.tests.factories.factory_role import RoleFactory

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory"""

    class Meta:
        model = "user.User"

    username = factory.LazyAttribute(lambda _: fake.user_name())
    password = factory.LazyAttribute(lambda _: fake.password())
    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    date_joined = factory.LazyAttribute(lambda _: fake.date_between_dates(timezone.now() - timezone.timedelta(days=365)))
    role = factory.SubFactory(RoleFactory)
