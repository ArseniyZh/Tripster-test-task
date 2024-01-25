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
    path("create/", PublicationCreateView.as_view()),
    path("update/<int:pk>/", PublicationUpdateView.as_view()),
    path("delete/<int:pk>/", PublicationDeleteView.as_view()),
    path("list/", PublicationListView.as_view()),

    path(vote + "create/", VoteCreateView.as_view(), ),
    path(vote + "update/<int:pk>/", VoteUpdateView.as_view(), ),
    path(vote + "delete/<int:pk>/", VoteDeleteView.as_view(), ),
]
