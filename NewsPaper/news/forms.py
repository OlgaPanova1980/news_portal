from django import forms
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text']


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        common_group, created = Group.objects.get_or_create(name='common')
        common_group.user_set.add(user)
        return user
