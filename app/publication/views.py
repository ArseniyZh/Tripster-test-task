from django.db.models import Sum, Count, Case, When, IntegerField
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from publication.models import Publication, Vote
from publication.permissions import PublicationBelongToUser, VoteBelongToUser
from publication.schemas import top_params
from publication.serializers import (
    PublicationListSerializer,
    PublicationSerializer,
    VoteCreateSerializer,
    VoteUpdateSerializer,
)


class PublicationCreateView(generics.CreateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PublicationUpdateView(generics.UpdateAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = (IsAuthenticated, PublicationBelongToUser,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class PublicationDeleteView(generics.DestroyAPIView):
    queryset = Publication.objects.all()
    permission_classes = (IsAuthenticated, PublicationBelongToUser,)


class PublicationListView(generics.ListAPIView):
    serializer_class = PublicationListSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        manual_parameters=top_params,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        top = int(self.request.GET.get("top", 10))
        top_publications = Publication.objects.annotate(
            rating=Sum(
                Case(
                    When(vote__vote=Vote.POSITIVE, then=1),
                    When(vote__vote=Vote.NEGATIVE, then=-1),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            votes_count=Count('vote', distinct=True),
        ).order_by("-rating")[:top]
        return top_publications


class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        publication_id = self.request.data.get("publication")
        publication = Publication.objects.get(id=publication_id)

        # Проверяем, голосовал ли пользователь за эту публикацию ранее
        existing_vote = Vote.objects.filter(user=user, publication=publication).first()
        if existing_vote:
            raise ValidationError({"detail": "You have already voted for this publication."})

        serializer.save(user=user, publication=publication)
        publication.refresh_from_db()  # Обновляем данные публикации после голосования
        return Response({"detail": "Vote has been recorded successfully."}, status=status.HTTP_201_CREATED)


class VoteUpdateView(generics.UpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteUpdateSerializer
    permission_classes = (IsAuthenticated, VoteBelongToUser,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class VoteDeleteView(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    permission_classes = (IsAuthenticated, VoteBelongToUser,)
