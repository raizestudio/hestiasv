import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory"""

    class Meta:
        model = "user.User"

    username = factory.LazyAttribute(lambda _: fake.user_name())
    password = factory.LazyAttribute(lambda _: fake.password())
    email = factory.LazyAttribute(lambda _: fake.email())
    # role = factory.LazyAttribute(lambda _: fake.random_element(elements=("user", "admin", "client", "driver")))
