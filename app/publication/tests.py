from typing import Dict

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from publication.models import Publication, Vote


@pytest.fixture
def api_client():
    return APIClient()


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


@pytest.fixture
def user_instance(test_user_data):
    return User.objects.create(**test_user_data)


@pytest.fixture
def publication_instance(user_instance):
    return Publication.objects.create(author=user_instance, text="Test text")


@pytest.fixture
def vote_instance(publication_instance):
    return Vote.objects.create(user=publication_instance.author, publication=publication_instance, vote=Vote.POSITIVE)


@pytest.mark.django_db
def test_create_publication_authenticated_user(api_client, user_instance):
    api_client.force_authenticate(user=user_instance)

    url = reverse("publication_create")
    data = {"text": "Test publication"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Publication.objects.filter(author=user_instance).count() == 1


@pytest.mark.django_db
def test_create_publication_unauthenticated_user(api_client):
    url = reverse("publication_create")
    data = {"text": "Test publication"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_publication_authenticated_user(api_client, user_instance):
    api_client.force_authenticate(user=user_instance)

    publication = Publication.objects.create(author=user_instance, text="Original text")

    url = reverse("publication_update", args=[publication.id])
    data = {"text": "Updated text"}
    response = api_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    publication.refresh_from_db()
    assert publication.text == "Updated text"


@pytest.mark.django_db
def test_update_publication_unauthenticated_user(api_client, user_instance):
    publication = Publication.objects.create(author=user_instance, text="Original text")

    url = reverse("publication_update", args=[publication.id])
    data = {"text": "Updated text"}
    response = api_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_publication_authenticated_user(api_client, user_instance):
    api_client.force_authenticate(user=user_instance)

    publication = Publication.objects.create(author=user_instance, text="Test text")

    url = reverse("publication_delete", args=[publication.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Publication.objects.filter(id=publication.id).exists()


@pytest.mark.django_db
def test_delete_publication_unauthenticated_user(api_client, user_instance):
    publication = Publication.objects.create(author=user_instance, text="Test text")

    url = reverse("publication_delete", args=[publication.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Publication.objects.filter(id=publication.id).exists()


@pytest.mark.django_db
def test_create_vote_authenticated_user(api_client, user_instance, publication_instance):
    api_client.force_authenticate(user=user_instance)

    url = reverse("vote_create")
    data = {"publication": publication_instance.id, "vote": Vote.POSITIVE}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Vote.objects.filter(user=user_instance).count() == 1


@pytest.mark.django_db
def test_create_vote_unauthenticated_user(api_client, user_instance, publication_instance):
    url = reverse("vote_create")
    data = {"publication": publication_instance.id, "vote": Vote.POSITIVE}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_vote_authenticated_user(api_client, user_instance, vote_instance):
    api_client.force_authenticate(user=user_instance)

    url = reverse("vote_update", args=[vote_instance.id])
    data = {"vote": Vote.NEGATIVE}
    response = api_client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    vote_instance.refresh_from_db()
    assert vote_instance.vote == Vote.NEGATIVE


@pytest.mark.django_db
def test_update_vote_unauthenticated_user(api_client, user_instance, vote_instance):
    url = reverse("vote_update", args=[vote_instance.id])
    data = {"vote": Vote.NEGATIVE}
    response = api_client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_vote_authenticated_user(api_client, user_instance, vote_instance):
    api_client.force_authenticate(user=user_instance)

    url = reverse("vote_delete", args=[vote_instance.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_vote_unauthenticated_user(api_client, user_instance, vote_instance):
    url = reverse("vote_delete", args=[vote_instance.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_change_publication_stats(user_instance, publication_instance):
    assert publication_instance.rating == 0
    assert publication_instance.votes_count == 0

    vote = Vote.objects.create(user=user_instance, publication=publication_instance, vote=Vote.POSITIVE)

    assert publication_instance.rating == 1
    assert publication_instance.votes_count == 1

    vote.vote = Vote.NEGATIVE
    vote.save()
    assert publication_instance.rating == -1

    vote.delete()
    assert publication_instance.rating == 0
    assert publication_instance.votes_count == 0
