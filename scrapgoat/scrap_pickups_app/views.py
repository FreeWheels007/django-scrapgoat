import django.forms
from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from datetime import datetime

from .forms import PickupForm, ProfileForm, UserSavedLocationForm, ListTextWidget, ChangeStatusForm
from .models import UserSavedLocation, Pickup


def index(request):
    # Post new pickup request
    if request.method == 'POST':
        pickup_form = PickupForm(request.POST, request.FILES)

        if pickup_form.is_valid():
            pickup = pickup_form.save(commit=False)
            # check if user is loggged in, not required
            pickup.user = request.user if request.user.is_authenticated else None
            pickup.save()
            return redirect('index')
    # Get template
    else:
        # Pre-populate form if user logged in
        if request.user.is_authenticated:
            address_query = UserSavedLocation.objects.filter(profile=request.user.profile).values()
            address_query = [value['address'] for value in address_query]
            pickup_form = PickupForm(instance=request.user.profile)
            pickup_form.fields['location'].widget = ListTextWidget(data_list=address_query, name='addresses',
                                                                   attrs={'class': 'form-control'})
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


# Collect user profile info to prefill pickup form
@login_required
def set_user_info(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        usl_form = UserSavedLocationForm(request.POST, instance=request.user.profile)

        if profile_form.is_valid():
            profile = profile_form.save()

            if usl_form.is_valid():
                usls = usl_form.save(commit=False)
                for usl in usls:
                    usl.profile = profile
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


# Allow moderators to view all posted pickup requests
@login_required
@permission_required('scrap_pickups_app.view_pickup', raise_exception=True)
def view_pickups(request, select):
    # View list of pickups
    if select in ('Pending', 'Completed', 'Cancelled'):
        if select == 'Pending':
            status = Pickup.Status.PENDING
        elif select == 'Completed':
            status = Pickup.Status.COMPLETED
        else:
            status = Pickup.Status.CANCELLED

        pickups = Pickup.objects.filter(status=status).order_by('-date_posted')

        content = {'pickups': pickups, 'select': select}

        return render(request, 'scrap_pickups_app/pickups.html', content)
    # Or view individual pickups
    else:
        try:
            pickup_id = int(select)
            pickup = Pickup.objects.get(id=pickup_id)
            cs_form = ChangeStatusForm(initial=model_to_dict(pickup))
            # print(f'cs form={cs_form}')
        except (Pickup.DoesNotExist, ValueError) as e:
            print('Exception in view_pickups')
            print(e)
            print('redirecting to index')
            return redirect('index')

        content = {'pickup': pickup, 'select': select, 'cs_form': cs_form}

        return render(request, 'scrap_pickups_app/pickup_details.html', content)


# Allow moderators to change pickup status
@login_required
@permission_required('scrap_pickups_app.change_pickup', raise_exception=True)
def change_pickup_status(request, select):
    if request.method == 'POST':
        try:
            pickup_id = int(select)
            pickup = Pickup.objects.get(id=pickup_id)
        except (Pickup.DoesNotExist, ValueError) as e:
            print('Exception in view_pickups')
            print(e)
            print('redirecting to index')
            return redirect('index')

        cs_form = ChangeStatusForm(request.POST, instance=pickup)
        if cs_form.is_valid():
            cs_form.save()
            print(datetime.now())
            pickup.date_finished = datetime.now()
            pickup.save(update_fields=['date_finished'])

        return redirect('view_pickups', select=select)
    else:
        return redirect('index')

