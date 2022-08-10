from django.forms import ModelForm, inlineformset_factory

from .models import Pickup, Profile, UserSavedLocation


class PickupForm(ModelForm):

    class Meta:
        model = Pickup
        fields = (
            'name',
            'email',
            'phone',
            'cell',
            'location',
            'details',
        )
        exclude = (
            'user',
            'status',
            'date_posted',
            'date_finished',
        )


class ProfileForm(ModelForm):

    class Meta:

        model = Profile
        fields = '__all__'
        exclude = (
            'user',
        )


UserSavedLocationForm = inlineformset_factory(
    Profile,
    UserSavedLocation,
    form=ProfileForm,
    fields=('address',),
    extra=1
)
