from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from tweets.views import TweetListView
from main.views import SerachView
from hashtags.api.views import TagTweetsListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('tweets.urls', namespace='tweets')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('hashtag/', include('hashtags.urls', namespace='hashtags')),
    path('', TweetListView.as_view(), name='home'),
    path('search/', SerachView.as_view(), name='search'),
    path('api/hashtag/<slug:tag>/', TagTweetsListAPIView.as_view(), name='hashtag'),
    path('api/tweets/', include('tweets.api.urls', namespace='tweetApi')),
    path('api/', include('accounts.api.urls', namespace='accountApi')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
