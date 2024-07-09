import factory
from faker import Faker

fake = Faker()


class MenuFactory(factory.django.DjangoModelFactory):
    """Menu factory"""

    class Meta:
        model = "core.Menu"

    name = factory.Sequence(lambda n: f"Menu {n}")
    description = factory.LazyAttribute(lambda _: fake.text())
    icon = factory.LazyAttribute(lambda _: fake.file_path())
    url = factory.LazyAttribute(lambda _: fake.uri())
    order = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))
