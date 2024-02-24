from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404


# Create your views here.
from blog.models import Post

from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm, Profile


@login_required
def dashboard(request):
    user=request.user
    posts = user.blog_posts.all()
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'posts': posts})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account:dashboard')
                else:
                    return JsonResponse({'Access denied': 'Disabled account'})
            else:
                return JsonResponse({'Invalid credentials': 'Invalid login'})
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():

            new_user = form.save(commit=False)

            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # Create a new user's Profile
            Profile.objects.create(user=new_user)
            return render(request, 'registration/registration_done.html', {'user_form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Profile updated successfully")
            return redirect('account:dashboard')

        messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
