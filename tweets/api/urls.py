from .views import (TweetListAPIView,
                    TweetAddAPIView,
                    RetweetApiView,
                    LikeToggleApiView,
                    TweetDetailAPIView,
                    TweetDeleteAPIView)
from django.urls import path
app_name = 'api'
urlpatterns = [
    path('', TweetListAPIView.as_view(), name='list'),
    path('add/', TweetAddAPIView.as_view(), name='add'),
    path('<int:pk>/like/', LikeToggleApiView.as_view(), name='like'),
    path('<int:pk>/delete/', TweetDeleteAPIView.as_view(), name='delete'),

    path('<int:pk>/retweet/', RetweetApiView.as_view(), name='retweet'),
    path('<int:pk>/', TweetDetailAPIView.as_view(), name='detail'),
]
