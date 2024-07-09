import factory
from faker import Faker

fake = Faker()


class ServiceFactory(factory.django.DjangoModelFactory):
    """Service factory"""

    class Meta:
        model = "service.Service"

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
