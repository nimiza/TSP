from django import forms
from .models import Location, Session, Customer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class LocationCreateEditForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of Your location'}))
    lat_lon = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'00.000000, 00.000000'}), label='Latitude, Longitude')

class CustomerCreateForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of Your location'}))
    shop_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of Your location'}))
    latitude = forms.FloatField(widget=forms.HiddenInput)
    longitude = forms.FloatField(widget=forms.HiddenInput)


class CustomerEditForm(forms.ModelForm):

    class Meta():
        model = Customer
        fields = [
            'name', 'shop_name', 'address', 'latitude', 'longitude'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Customer Name'}),
            'shop_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of Your Shop'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Your Address'}),
            'latitude': forms.TextInput(attrs={'class':'form-control', 'placeholder':'00.000000'}),
            'longitude': forms.TextInput(attrs={'class':'form-control', 'placeholder':'00.000000'}),
        }
        labels = {
            'shop_name': 'Shop Name',
        }

class SessionCreateEditForm(forms.ModelForm):

    customer = forms.ModelMultipleChoiceField(queryset=Customer.objects.all(), widget=Select2MultipleWidget(attrs={'class': 'form-control select2', 'data-placeholder': 'Select Customers...'}), required=True)

    class Meta():
        model = Session
        fields = [
            'name', 'customer'
        ]


        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of Your session'}),
        }

        # customer = forms.ModelMultipleChoiceField(queryset=Customer.objects.all())
        # widget = forms.SelectMultiple(attrs={'class': 'select2'})


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This Username Exists!')
        return username


















# class LocationForm(forms.ModelForm):
#     class Meta():
#         model = Location
#         fields = [
#             'name', 'latitude', 'longitude'
#             ]
#         widgets = {
#             'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of Your location'}),
#             'latitude': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'00.000000'}),
#             'longitude': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'00.000000'})
#         }