from django.shortcuts import render
from django.views import View

from .models import Hashtag

class HashtagView(View):
	def get(self,request,hashtag):
		hashtag,created = Hashtag.objects.get_or_create(tag=hashtag)
		return render(request,'hashtags/hashtag.html',{'obj':hashtag}) 
