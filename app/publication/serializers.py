from rest_framework import serializers

from publication.models import Publication, Vote


class PublicationListSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=False, read_only=True)
    votes_count = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Publication
        fields = "__all__"


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ("text",)


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("publication", "vote",)


class VoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("vote",)
