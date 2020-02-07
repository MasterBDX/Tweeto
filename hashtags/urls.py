from django.urls import path

from .views import (HashtagView)


app_name = 'hashtags'
urlpatterns = [
    path('<slug:hashtag>/',HashtagView.as_view(),name='name')
]
