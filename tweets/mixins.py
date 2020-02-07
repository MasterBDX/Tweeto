from django import forms
from django.forms.utils import ErrorList
from django.core.exceptions import PermissionDenied

class MustLoggedInMixin(object):
	def form_valid(self,form):
		user = self.request.user
		if user.is_authenticated:
			form.instance.user = user
			return super().form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['User must be logged in to tweet'])
					
			return self.form_invalid(form)


class UserOwnerMixin(object):
	def get_object(self,queryset=None):
		obj = super().get_object(queryset=None)
		user = self.request.user
		if obj.user != user:
			raise PermissionDenied()
		else:
			return obj