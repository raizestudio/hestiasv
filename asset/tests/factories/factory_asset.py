import factory
from faker import Faker

fake = Faker()


class AssetFactory(factory.django.DjangoModelFactory):
    """Asset factory"""

    class Meta:
        model = "asset.asset"

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    is_active = factory.LazyAttribute(lambda _: fake.boolean())
    slug = factory.LazyAttribute(lambda _: fake.slug())
