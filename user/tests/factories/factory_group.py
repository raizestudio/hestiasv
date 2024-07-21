import factory
from faker import Faker

fake = Faker()


class GroupFactory(factory.django.DjangoModelFactory):
    """Group factory"""

    class Meta:
        model = "user.Group"

    code = factory.LazyAttribute(lambda _: f"GR-{''.join(fake.random_letters(length=3))}")
    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
    color = factory.LazyAttribute(lambda _: fake.color_name())
    slug = factory.LazyAttribute(lambda _: fake.slug())
