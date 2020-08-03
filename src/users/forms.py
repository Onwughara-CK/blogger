from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class ExtendedUserCreationForm(UserCreationForm):
    """
    adds email field to default UserCreationForm
    """
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    """
    use to update profile details
    """
    class Meta:
        model = User
        fields = ('email', 'username')


class UpdatePictureForm(forms.ModelForm):
    """
    use to update profile picture
    """
    class Meta:
        model = Profile
        fields = ('image',)
