import factory
from faker import Faker

fake = Faker()


class AppSettingFactory(factory.django.DjangoModelFactory):
    """AppSetting factory"""

    class Meta:
        model = "core.appSetting"

    key = factory.LazyAttribute(lambda _: fake.name())
    value = factory.LazyAttribute(lambda _: fake.word())
