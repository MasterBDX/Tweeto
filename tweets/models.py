from django.db import models
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from django_resized import ResizedImageField

from .utils import get_tweet_image_name
from .validators import validate_content


class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            parent_obj = parent_obj.parent

        qs = Tweet.objects.filter(user=user, parent=parent_obj,
                                  timestamp__date=timezone.now(),
                                  reply=False)
        if qs.exists():
            return None
        obj = self.model(user=user,
                         parent=parent_obj,
                         content=parent_obj.content)
        obj.save()
        return obj

    def like_toggle(self, user, tweet):
        if user in tweet.liked.all():
            is_like = False
            tweet.liked.remove(user)
        else:
            is_like = True
            tweet.liked.add(user)
        return is_like


User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    content = models.CharField(max_length=255, validators=[validate_content])
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True)
    liked = models.ManyToManyField(User, related_name='liked',
                                   blank=True)
    image = ResizedImageField(size=[500, 300],
                              upload_to=get_tweet_image_name, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reply = models.BooleanField(verbose_name='Is a reply?', default=False)

    objects = TweetManager()

    def __str__(self):
        if self.parent and self.reply:
            return '(reply via ' + self.user.username + ')'
        elif self.parent:
            return ' (retweeted via ' + self.user.username + ')'
        return self.user.username

    def get_absolute_url(self):
        return reverse('tweets:detail', kwargs={'pk': self.pk})

    def get_parent(self):
        parent = self
        if self.parent:
            parent = self.parent
        return parent

    def get_children(self):
        parent = self.get_parent()
        qs1 = Tweet.objects.filter(parent=parent)
        qs2 = Tweet.objects.filter(pk=parent.pk)
        return (qs1 | qs2)
