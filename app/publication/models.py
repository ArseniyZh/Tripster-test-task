from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import User


class Publication(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def votes_count(self):
        return Vote.objects.filter(publication=self).count()

    def rating(self):
        queryset = Vote.objects.filter(publication=self)
        rating = queryset.filter(vote=Vote.POSITIVE).count() - queryset.filter(vote=Vote.NEGATIVE).count()
        return rating


class Vote(BaseModel):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    vote_choices = (
        (POSITIVE, POSITIVE),
        (NEGATIVE, NEGATIVE),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    vote = models.CharField(max_length=8, choices=vote_choices)
