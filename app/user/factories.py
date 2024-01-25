import factory
from faker import Factory as FakerFactory
from django.contrib.auth.models import User

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.user_name())
    password = factory.PostGenerationMethodCall('set_password', faker.password())
