from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

from .serializers import TweetModelSerializer
from tweets.models import Tweet
from .pagination import StandardTweetsPagination
from accounts.models import UserProfile


class LikeToggleApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        user = request.user
        tweet = get_object_or_404(Tweet, pk=pk)
        liked_tweet = Tweet.objects.like_toggle(user, tweet)
        liked_num = tweet.liked.all().count()
        return Response({'liked': liked_tweet,
                         'likedNum': liked_num})


class ProfileLikeToggleApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, slug, format=None):
        user = request.user
        tweet = get_object_or_404(Tweet, pk=pk)
        liked_tweet = Tweet.objects.like_toggle(user, tweet)
        # data = TweetModelSerializer(liked_tweet).data
        return Response({'liked': liked_tweet})


class RetweetApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        user = request.user
        msg = 'Not allowed'
        tweet = get_object_or_404(Tweet, pk=pk, user=user)
        retweet = Tweet.objects.retweet(user, tweet)
        if retweet is not None:
            data = TweetModelSerializer(
                retweet, context={'request': request}).data
            return Response(data)
            msg = 'you can\'t retweet the same in 1 day '
        return Response({'message': msg, 'id': tweet.id}, status=400)


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardTweetsPagination

    def get_queryset(self):
        q = self.request.GET.get('q')
        user = self.request.user
        filters = Q(content__iexact='fhgt$$dge#wr$$*HGF')
        slug = self.kwargs.get('user_slug')
        if user.is_authenticated:
            users = user.profile.get_following()
            filters = Q(user__in=users) | Q(user=user)
        else:
            q = ' '

        if slug:
            filters = Q(user__slug=slug)

        if q is not None and q != '':
            filters = Q(content__icontains=q) | Q(user__username__icontains=q)

        qs = Tweet.objects.filter(filters).distinct().order_by('-timestamp')
        return qs

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class TweetAddAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetDeleteAPIView(generics.DestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj.user != user:
            raise Http404
        return obj


class TweetDetailAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardTweetsPagination

    def get_queryset(self, *args, **kwargs):
        tweet_id = self.kwargs.get('pk')
        qs = Tweet.objects.filter(pk=tweet_id)
        if qs.exists() and qs.count() == 1:
            parent = qs.first()
            qs1 = parent.get_children()
            qs = (qs | qs1).distinct().extra(
                select={'parent_is_null': 'parent_id IS NULL'})
        return qs.order_by('-parent_is_null', 'timestamp')
