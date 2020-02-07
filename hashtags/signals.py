from django.dispatch import Signal, receiver
from tweets.models import Tweet
from .models import Hashtag
parsed_hashtags = Signal(providing_args=['hashtaglist'])


@receiver(parsed_hashtags, sender=Tweet)
def parsed_hashtags_receiver(sender, hashtaglist, *args, **kwargs):
    if len(hashtaglist) > 0:
        for tag in hashtaglist:
            hashtag, created = Hashtag.objects.get_or_create(tag=tag)
