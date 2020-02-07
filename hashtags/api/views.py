from rest_framework import generics
from rest_framework import permissions
from django.db.models import Q


from tweets.api.serializers import TweetModelSerializer
from tweets.api.pagination import StandardTweetsPagination
from hashtags.models import Hashtag


class TagTweetsListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardTweetsPagination

    def get_queryset(self, *args, **kwargs):
        tag = self.kwargs.get('tag')
        obj = Hashtag.objects.filter(tag=tag).first()
        qs = []
        if obj:
            qs = obj.get_tweets()
        return qs

        # q = self.request.GET.get('q')
        # user = self.request.user
        # filters = Q(content__iexact='fhgt$$dge#wr$$*HGF')
        # slug = self.kwargs.get('user_slug')
        # if user.is_authenticated:
        #     users = user.profile.get_following()
        #     filters = Q(user__in=users) | Q(user=user)
        # else:
        #     q = ' '
        # if slug:
        #     filters = Q(user__slug=slug)
        # if q is not None and q != '':
        #     filters = Q(content__icontains=q) | Q(user__username__icontains=q)

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context
