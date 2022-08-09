from django.forms import ModelForm

from .models import Pickup, Profile


class PickupForm(ModelForm):

    class Meta:
        model = Pickup
        fields = [
            'name',
            'email',
            'phone',
            'cell',
            'location',
            'details',
        ]
        exclude = [
            'user',
            'status',
            'date_posted',
            'date_finished',
        ]


class ProfileForm(ModelForm):

    class Meta:

        model = Profile
        fields = [
            'name',
            'phone',
            'cell',
        ]
