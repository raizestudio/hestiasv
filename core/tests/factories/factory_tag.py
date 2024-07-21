import factory
from faker import Faker

fake = Faker()


class TagFactory(factory.django.DjangoModelFactory):
    """Tag factory"""

    class Meta:
        model = "core.Tag"

    name = factory.LazyAttribute(lambda _: fake.name())
    color = factory.LazyAttribute(lambda _: fake.color_rgb())
