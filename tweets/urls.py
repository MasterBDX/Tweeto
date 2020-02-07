from django.urls import path
from django.views.generic.base import RedirectView
from .views import (TweetListView,
                    TweetDetailView,
                    TweetCreateView,
                    TweetEditView,
                    TweetDeleteView,
                    RetweetView)

app_name = 'tweets'
urlpatterns = [
    path('', RedirectView.as_view(url='/')),
    path('search/', TweetListView.as_view(), name='list'),
    path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
    path('<int:pk>/retweet/', RetweetView.as_view(), name='retweet'),
    path('edit/<int:pk>/', TweetEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', TweetDeleteView.as_view(), name='delete'),
]
