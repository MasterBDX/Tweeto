from django import forms

from .models import Tweet
from django.core import validators


class AddTweetForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea(attrs={'placeholder': 'What\'s Happening',
                                                           'class': 'form-control'}),
                              validators=[validators.MaxLengthValidator(255)]

                              )
    image = forms.ImageField(label='', required=False)

    class Meta:
        model = Tweet
        fields = ['content', 'image']
