from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class SerachView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        qs = None
        if q:
            qs = User.objects.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q))
        return render(request, 'main/results.html', {'users': qs})
