from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text']

    from allauth.account.forms import SignupForm
    from django.contrib.auth.models import Group

    class CommonSignupForm(SignupForm):

        def save(self, request):
            user = super(CommonSignupForm, self).save(request)
            common_group = Group.objects.get(name='common')
            common_group.user_set.add(user)
            return user