from typing import Dict

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def user_instance():
    user = UserFactory()
    return user


@pytest.fixture
def test_user_data() -> Dict[str, str]:
    """
    Тестовые данные юзера

    :return: Словарь с username и password
    :rtype: Dict[str, str]
    """
    return {
        "username": "testuser",
        "password": "testpassword",
    }


@pytest.mark.django_db
def test_registration(api_client, test_user_data):
    response = api_client.post(reverse("register"), data=test_user_data)

    # Проверяем, что ответ имеет код 201 CREATED
    assert response.status_code == status.HTTP_201_CREATED

    # Проверяем, что в ответе есть токен
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login(api_client, test_user_data):
    User.objects.create_user(**test_user_data)

    response = api_client.post(reverse("login"), data=test_user_data)

    # Проверяем, что ответ имеет код 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что в ответе есть токен
    assert 'access' in response.data
    assert 'refresh' in response.data
