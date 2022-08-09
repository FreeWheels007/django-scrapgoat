from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from .forms import PickupForm, ProfileForm


def index(request):
    if request.method == 'POST':
        pickup_form = PickupForm(request.POST)

        if pickup_form.is_valid():
            pickup = pickup_form.save(commit=False)
            print(f'user={request.user}')
            pickup.user = request.user if request.user.is_authenticated else None
            pickup.save()
            redirect('index')
    else:
        pickup_form = PickupForm()

    content = {'form': pickup_form}

    return render(request, 'scrap_pickups_app/index.html', content)


@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://localhost:8000'  # this can be current domain
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')


@login_required
def set_user_info(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
    else:
        profile_form = ProfileForm(initial=model_to_dict(request.user), instance=request.user.profile)

    content = {'form': profile_form}

    return render(request, 'scrap_pickups_app/profile.html', content)
