import re
from django.db.models.signals import post_save
from django.dispatch import receiver

from hashtags.signals import parsed_hashtags
from .models import Tweet


@receiver(post_save, sender=Tweet)
def tweet_save(sender, instance, created, *args, **kwargs):
    user_regex = r'@(?P<username>[\w.@+-]+)'
    usernames = re.findall(user_regex, instance.content)

    hashtag_regex = r'#(?P<hashtag>[\w\d-]+)'
    hashtags = re.findall(hashtag_regex, instance.content)
    parsed_hashtags.send(sender=instance.__class__,
                         hashtaglist=hashtags,

                         )
