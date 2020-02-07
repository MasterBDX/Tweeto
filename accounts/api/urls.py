from tweets.api.views import TweetListAPIView

from django.urls import path
app_name = 'api'
urlpatterns = [
    path('<slug:user_slug>/tweets/',
         TweetListAPIView.as_view(),
         name='profile_tweets'),

]
