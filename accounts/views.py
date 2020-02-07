from django.views.generic import DetailView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView)
from django.views import View
from django.views.generic import (ListView, CreateView, DetailView, UpdateView)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseForbidden

from .forms import (LoginForm, RegistrationForm,
                    UserProfileForm, UserProfileColorForm)
from .models import UserProfile
from .mixins import AnonymousRequiredMixin


User = get_user_model()


class UserLoginView(AnonymousRequiredMixin, LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', None)
        login(self.request, form.get_user())
        if remember_me:
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = 'accounts:login'


class UserProfileView(DetailView):
    queryset = User.objects.all()
    template_name = 'accounts/profile.html'
    slug_url_kwarg = 'user_slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = self.request.user
        context['me'] = False

        if user.is_authenticated:
            if user.slug == context['object'].slug:
                context['me'] = True
            context['is_followed'] = UserProfile.objects.is_following(
                self.request.user, self.get_object())
        return context


class UserRegistrerView(AnonymousRequiredMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/'


class UserFollow(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def get(self, request, user_slug, *args, **kwargs):
        user_following = get_object_or_404(User, slug=user_slug)

        if request.user.is_authenticated:
            follow_user = UserProfile.objects.toggle_follow(
                request.user, user_following)
            if request.is_ajax():
                user_status = 'Follow'
                if follow_user:
                    user_status = 'Unfollow'
                user_followers_num = user_following.followed_by.count()
                data = {'usrst': user_status,
                        'ufn': user_followers_num}
                return JsonResponse(data)
        return redirect('accounts:profile', user_slug=user_slug)


class FollowManager(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def get(self, request, user_slug, *args, **kwargs):
        user_following = get_object_or_404(User, slug=user_slug)
        if request.user.is_authenticated:
            follow_user = UserProfile.objects.toggle_follow(
                request.user, user_following)
            if request.is_ajax():
                user_status = 'Follow'
                if follow_user:
                    user_status = 'Unfollow'
                data = {'usrst': user_status}
                return JsonResponse(data)
        return redirect('accounts:following', user_slug=request.user.slug)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    queryset = UserProfile.objects.all()
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        profile = self.request.user.profile
        if obj != profile:
            raise Http404
        return obj


class FollowersView(DetailView):
    queryset = User.objects.all()
    template_name = 'accounts/followers.html'
    slug_url_kwarg = 'user_slug'
    context_object_name = 'obj'


class FollowingView(DetailView):
    queryset = User.objects.all()
    template_name = 'accounts/following.html'
    slug_url_kwarg = 'user_slug'
    context_object_name = 'obj'


class ThemeChange(LoginRequiredMixin, View):
    login_url = '/account/login/'

    def get(self, request):
        return redirect('/')

    def post(self, request):
        path = request.POST.get('current_path')
        if not path:
            path = '/'
        form = UserProfileColorForm(
            request.POST or None, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect(path)
