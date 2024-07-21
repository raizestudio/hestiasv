import factory
from faker import Faker

fake = Faker()
from user.tests.factories.factory_group import GroupFactory


class RoleFactory(factory.django.DjangoModelFactory):
    """Role factory"""

    class Meta:
        model = "user.Role"

    code = factory.LazyAttribute(lambda _: f"RO-{''.join(fake.random_letters(length=3))}")
    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    slug = factory.LazyAttribute(lambda _: fake.slug())

    group = factory.SubFactory(GroupFactory)
