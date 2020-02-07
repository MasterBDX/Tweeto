from rest_framework import serializers
# from django.template.defaultfilters import timesince
from django.utils.timesince import timesince
from django.urls import reverse_lazy

from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer


class RetweetModelSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    display_date = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    likes_num = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    user = UserDisplaySerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'timesince', 'url', 'is_like',
                  'display_date', 'follower_count', 'likes_num', 'reply', ]

    def get_follower_count(self, obj):
        return 0

    def get_display_date(self, obj):
        return obj.timestamp.strftime("| %b %d, %Y | %I:%M %p ")

    def get_is_like(self, obj):
        user = self.context.get('request').user
        if user in obj.liked.all():
            return 'Unliked'
        return 'Liked'

    def get_likes_num(self, obj):
        num = obj.liked.all().count()
        return num

    def get_timesince(self, obj):
        timestamp = obj.timestamp
        return timesince(timestamp) + ' ago'

    def get_url(self, obj):
        return reverse_lazy('accounts:profile', kwargs={'user_slug': obj.user.slug})


class TweetModelSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(required=False,
                                      write_only=True)
    follower_count = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    display_date = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    likes_num = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    my_tweet = serializers.SerializerMethodField()

    user = UserDisplaySerializer(read_only=True)
    parent = RetweetModelSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'image',
                  'parent_id', 'reply', 'timesince',
                  'url', 'is_like', 'display_date',
                  'follower_count', 'parent', 'likes_num', 'my_tweet']

        # read_only_fields = ['reply']

    def get_follower_count(self, obj):
        return 0

    def get_is_like(self, obj):
        user = self.context.get('request').user
        if user in obj.liked.all():
            return 'Unliked'
        return 'Liked'

    def get_likes_num(self, obj):
        num = obj.liked.all().count()
        return num

    def get_display_date(self, obj):
        return obj.timestamp.strftime("| %b %d, %Y | %I:%M %p ")

    def get_timesince(self, obj):
        timestamp = obj.timestamp
        return timesince(timestamp) + ' ago'

    def get_my_tweet(self, obj):
        user = self.context.get('request').user
        if user == obj.user:
            return True
        return False

    def get_url(self, obj):
        return reverse_lazy('accounts:profile', kwargs={'user_slug': obj.user.slug})
