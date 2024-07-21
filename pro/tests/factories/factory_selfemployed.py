import factory
from faker import Faker

fake = Faker()


class SelfEmployedFactory(factory.django.DjangoModelFactory):
    """SelfEmployed factory"""

    class Meta:
        model = "pro.SelfEmployed"

    name = factory.LazyAttribute(lambda _: fake.word())
    legal_status = factory.LazyAttribute(lambda _: fake.word())
    siret = factory.LazyAttribute(lambda _: fake.word())
    siren = factory.LazyAttribute(lambda _: fake.word())
    creation_date = factory.LazyAttribute(lambda _: fake.date())
    slug = factory.LazyAttribute(lambda _: fake.word())
