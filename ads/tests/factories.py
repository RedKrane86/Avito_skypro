import factory

from ads.models import Ad, User, Category


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('name')
    password = factory.Faker('password')
    email = factory.Faker('email')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker('name')
    slug = factory.Faker('ean', length=8)


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad
    name = factory.Faker('name')
    price = 100
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
