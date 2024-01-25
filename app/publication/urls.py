from django.urls import path

from publication.views import (
    PublicationCreateView,
    PublicationUpdateView,
    PublicationDeleteView,
    PublicationListView,

    VoteCreateView,
    VoteUpdateView,
    VoteDeleteView,
)

vote = "vote/"

urlpatterns = [
    path("create/", PublicationCreateView.as_view(), name="publication_create"),
    path("update/<int:pk>/", PublicationUpdateView.as_view(), name="publication_update"),
    path("delete/<int:pk>/", PublicationDeleteView.as_view(), name="publication_delete"),
    path("list/", PublicationListView.as_view(), name="publication_list"),

    path(vote + "create/", VoteCreateView.as_view(), name="vote_create"),
    path(vote + "update/<int:pk>/", VoteUpdateView.as_view(), name="vote_update"),
    path(vote + "delete/<int:pk>/", VoteDeleteView.as_view(), name="vote_delete"),
]
