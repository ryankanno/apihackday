from django.forms import ModelForm
from fans.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
