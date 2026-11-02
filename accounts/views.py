from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from .forms import ProfileForm, RegisterForm, UserForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            user = form.save()
            Profile.objects.create(user=user)
        login(request, user)
        messages.success(request, 'Tu cuenta está lista. ¡Bienvenido a Bitácora Tech!')
        return redirect('blog:post_list')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {
        'profile': profile, 'posts': request.user.posts.all(),
    })


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST':
        user_valid = user_form.is_valid()
        profile_valid = profile_form.is_valid()
        if user_valid and profile_valid:
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            messages.success(request, 'Tu perfil se actualizó.')
            return redirect('accounts:profile')
    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form, 'profile_form': profile_form,
    })
