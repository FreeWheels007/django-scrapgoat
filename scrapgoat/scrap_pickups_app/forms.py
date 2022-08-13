from django.forms import ModelForm, inlineformset_factory, TextInput
from django import forms
from .models import Pickup

from .models import Pickup, Profile, UserSavedLocation


class ListTextWidget(TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return text_html + data_list


class PickupForm(ModelForm):

    class Meta:
        model = Pickup
        fields = (
            'name',
            'email',
            'cell',
            'phone',
            'location',
            'details',
            'scrap_image',
        )
        exclude = (
            'user',
            'status',
            'date_posted',
            'date_finished',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'cell': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class ProfileForm(ModelForm):

    class Meta:

        model = Profile
        fields = (
            'name',
            'email',
            'cell',
            'phone',
        )
        exclude = (
            'user',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'cell': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


UserSavedLocationForm = inlineformset_factory(
    Profile,
    UserSavedLocation,
    form=ProfileForm,
    fields=('address',),
    extra=1,
    widgets={'address': forms.TextInput(attrs={'class': 'form-control'})}
)


class ChangeStatusForm(ModelForm):

    class Meta:

        model = Pickup
        fields = ('status',)
        exclude = '__all__'
        widgets = {'status': forms.RadioSelect}
