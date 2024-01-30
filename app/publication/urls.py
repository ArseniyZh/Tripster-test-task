from django.urls import path, include
from rest_framework.routers import DefaultRouter
from publication.views import PublicationViewSet, VoteViewSet

router = DefaultRouter()
router.register(r"publication", PublicationViewSet, basename="publication")
router.register(r"vote", VoteViewSet, basename="vote")

urlpatterns = [
    path("", include(router.urls)),
]
