from django.db.models import Sum, Count, Case, When, IntegerField
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from publication.models import Publication, Vote
from publication.permissions import PublicationBelongToUser, VoteBelongToUser
from publication.schemas import top_params
from publication.serializers import (
    PublicationListSerializer,
    PublicationSerializer,
    VoteCreateSerializer,
    VoteUpdateSerializer,
    VoteSerializer,
)


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    permission_classes = (IsAuthenticated, PublicationBelongToUser,)

    def get_serializer_class(self):
        if self.action in ["list"]:
            return PublicationListSerializer
        return PublicationSerializer

    @swagger_auto_schema(manual_parameters=top_params)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        top = request.GET.get("top")
        created_at = request.GET.get("created_at")

        if created_at:
            queryset = queryset.filter(created_at=int(created_at))
        if top:
            queryset = queryset.annotate(
                rating=Sum(
                    Case(
                        When(vote__vote=Vote.POSITIVE, then=1),
                        When(vote__vote=Vote.NEGATIVE, then=-1),
                        default=0,
                        output_field=IntegerField()
                    )
                ),
                votes_count=Count("vote", distinct=True),
            ).order_by("-rating")[:int(top)]

        serializer = PublicationListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    permission_classes = (IsAuthenticated, VoteBelongToUser,)

    def get_serializer_class(self):
        if self.action == "create":
            return VoteCreateSerializer
        elif self.action == "update":
            return VoteUpdateSerializer
        return VoteSerializer

    def perform_create(self, serializer):
        user = self.request.user
        publication_id = self.request.data.get("publication")
        publication = Publication.objects.get(id=publication_id)

        existing_vote = Vote.objects.filter(user=user, publication=publication).first()
        if existing_vote:
            raise ValidationError({"detail": "You have already voted for this publication."})

        serializer.save(user=user, publication=publication)
        publication.refresh_from_db()
        return Response({"detail": "Vote has been recorded successfully."}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        vote = self.get_object()
        publication = vote.publication
        user = self.request.user

        if vote.user != user:
            raise PermissionDenied({"detail": "You don't have permission to undo this vote."})

        vote.delete()
        publication.refresh_from_db()
        return Response({"detail": "Vote has been undone successfully."}, status=status.HTTP_200_OK)
