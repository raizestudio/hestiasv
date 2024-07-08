import factory
from faker import Faker

fake = Faker()

from core.tests.factories.factory_menu import MenuFactory


class MenuItemFactory(factory.django.DjangoModelFactory):
    """Menu Item factory"""

    class Meta:
        model = "core.MenuItem"

    name = factory.Sequence(lambda n: f"Menu Item {n}")
    description = factory.LazyAttribute(lambda _: fake.text())
    icon = factory.LazyAttribute(lambda _: fake.file_path())
    url = factory.LazyAttribute(lambda _: fake.uri())
    order = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))

    menu = factory.SubFactory(MenuFactory)
