from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms


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
            return redirect('page:home')
    else:
        form = forms.ExtendedUserCreationForm()
    return render(request, 'page/register.html', {'form': form})
