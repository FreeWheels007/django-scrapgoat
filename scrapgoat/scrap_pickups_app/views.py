import django.forms
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from .forms import PickupForm, ProfileForm, UserSavedLocationForm
from .models import UserSavedLocation


def index(request):
    if request.method == 'POST':
        pickup_form = PickupForm(request.POST)

        if pickup_form.is_valid():
            pickup = pickup_form.save(commit=False)
            print(f'user={request.user}')
            pickup.user = request.user if request.user.is_authenticated else None
            pickup.save()
            return redirect('index')
    else:
        if request.user.is_authenticated:
            address_query = UserSavedLocation.objects.filter(profile=request.user.profile).values()
            address_query = [(value['id'], value['address']) for value in address_query]
            print(f'query into intit = {address_query}')
            pickup_form = PickupForm(instance=request.user.profile)
            pickup_form.fields['location'] = django.forms.ChoiceField(choices=address_query)
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
        usl_form = UserSavedLocationForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile = profile_form.save()

            if usl_form.is_valid():
                usls = usl_form.save(commit=False)
                print(usls)
                for usl in usls:
                    usl.profile = profile
                    print(model_to_dict(usl))
                    usl.save()

            for usl in usl_form.deleted_objects:
                usl.delete()

        return redirect('profile_info')

    else:
        profile_form = ProfileForm(initial=model_to_dict(request.user), instance=request.user.profile)
        usl_form = UserSavedLocationForm(queryset=UserSavedLocation.objects
                                         .filter(profile=request.user.profile), instance=request.user.profile)

    content = {'form': profile_form, 'usls': usl_form}

    return render(request, 'scrap_pickups_app/profile.html', content)
