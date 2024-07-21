import factory
from faker import Faker

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    """Category factory"""

    class Meta:
        model = "core.Category"

    name = factory.LazyAttribute(lambda _: fake.name())
