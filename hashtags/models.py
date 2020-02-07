from django.db import models
from django.urls import reverse
from tweets.models import Tweet


class Hashtag(models.Model):
    tag = models.CharField(max_length=155)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('hashtag:name', kwargs={'hashtag': self.tag})

    def get_tweets(self):
        return Tweet.objects.filter(content__icontains='#' + self.tag)
