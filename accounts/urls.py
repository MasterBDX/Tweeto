from django.urls import path


from .views import (UserLoginView, UserRegistrerView, UserProfileUpdateView,
                    UserLogoutView, UserProfileView, UserFollow, ThemeChange,
                    FollowManager, FollowingView, FollowersView)
from tweets.api.views import ProfileLikeToggleApiView


app_name = 'accounts'
urlpatterns = [

    path('theme/', ThemeChange.as_view(), name='theme'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrerView.as_view(), name='register'),
    path('<slug:user_slug>/follow/', UserFollow.as_view(), name='follow'),
    path('<slug:user_slug>/follow_manage/',
         FollowManager.as_view(), name='follow_manage'),
    path('<slug:user_slug>/', UserProfileView.as_view(), name='profile'),
    path('<int:pk>/edit/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('<slug:user_slug>/followers/',
         FollowersView.as_view(), name='followers'),
    path('<slug:user_slug>/following/',
         FollowingView.as_view(), name='following'),
    path('<slug:slug>/api/tweets/<int:pk>/like/',
         ProfileLikeToggleApiView.as_view(), name='user-like'),
]
