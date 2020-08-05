from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . import forms, models
from page.models import Post


def register(request):
    """
    returns registration form
    """
    if request.method == 'POST':
        form = forms.ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'successfully created account for {username}')
            return redirect('login')
    else:
        form = forms.ExtendedUserCreationForm()
    return render(request, 'page/register.html', {'form': form})


@login_required
def profile(request, username):
    if request.method == 'POST':
        form_profile = forms.UpdateProfileForm(
            request.POST,
            instance=request.user
        )
        form_picture = forms.UpdatePictureForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if form_profile.is_valid() and form_picture.is_valid():
            form_picture.save()
            form_profile.save()
            messages.success(
                request,
                f'You have successfully updated your account'
            )
            return redirect('profile')
    else:
        user = User.objects.get(username=username)
        context = {
            'profile_owner': user
        }
        if request.user == user:
            form_picture = forms.UpdatePictureForm(
                instance=user.profile)
            form_profile = forms.UpdateProfileForm(instance=user)

            context.update({
                "form_pic": form_picture,
                "form_pro": form_profile
            })

    return render(request, 'page/profile.html', context)



