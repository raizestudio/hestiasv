import factory
from faker import Faker

fake = Faker()

from core.tests.factories.factory_category import CategoryFactory
from core.tests.factories.factory_tag import TagFactory


class ServiceFactory(factory.django.DjangoModelFactory):
    """Service factory"""

    class Meta:
        model = "service.Service"

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    is_active = factory.LazyAttribute(lambda _: fake.boolean())
    estimated_duration = factory.LazyAttribute(lambda _: fake.time())
    slug = factory.LazyAttribute(lambda _: fake.slug())
