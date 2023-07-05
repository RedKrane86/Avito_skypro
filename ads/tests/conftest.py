from pytest_factoryboy import register

from ads.tests.factories import AdFactory, UserFactory, CategoryFactory

pytest_plugins = 'ads.tests.fixtures'

register(AdFactory)
register(UserFactory)
register(CategoryFactory)
