from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import View

from .mixins import (MustLoggedInMixin, UserOwnerMixin)
from .forms import AddTweetForm
from .models import Tweet


class TweetListView(generic.ListView):
    context_object_name = 'tweets'
    template_name = 'main/home.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q is not None:
            filters = Q(content__icontains=q) | Q(user__username__icontains=q)
            qs = Tweet.objects.filter(filters)
            return qs
        qs = Tweet.objects.all()
        return qs

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        context['create_form'] = AddTweetForm()

        return context


class TweetDetailView(generic.DetailView):
    model = Tweet
    fileds = '__all__'
    context_object_name = 'tweet'
    template_name = 'tweets/tweet_details.html'


class TweetCreateView(MustLoggedInMixin, generic.CreateView):
    form_class = AddTweetForm
    template_name = 'tweets/add_tweet.html'


class TweetEditView(LoginRequiredMixin, UserOwnerMixin, generic.UpdateView):
    form_class = AddTweetForm
    queryset = Tweet.objects.all()
    success_url = reverse_lazy('home')
    template_name = 'tweets/tweet_edit.html'


class TweetDeleteView(LoginRequiredMixin, UserOwnerMixin, generic.DeleteView):
    model = Tweet
    success_url = reverse_lazy('home')
    template_name = 'tweets/tweet_delete_confirm.html'


class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        user = request.user
        if user.is_authenticated:
            new_tweet = Tweet.objects.retweet(user, tweet)
            return redirect('/')
        else:
            return redirect('/')
