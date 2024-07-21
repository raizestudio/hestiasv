import factory
from faker import Faker

from pro.tests.factories.factory_enterprise import EnterpriseFactory
from user.tests.factories.factory_base_user import UserFactory

fake = Faker()


class EnterpriseMemberFactory(factory.django.DjangoModelFactory):
    """Enterprise factory"""

    class Meta:
        model = "pro.EnterpriseMember"

    user = factory.SubFactory(UserFactory)
    position = factory.LazyAttribute(lambda _: fake.job())
    date_joined = factory.LazyAttribute(lambda _: fake.date())
    enterprise = factory.SubFactory(EnterpriseFactory)
