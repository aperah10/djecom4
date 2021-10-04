from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *

#  USER CREATION FORM
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("phone",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "phone",
            "email",
            "fullname",
        )


# ------------ ----- SIGNUP FORM PART ---------------------


class RegisterForm(forms.ModelForm):
    phone = forms.IntegerField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    country_code = forms.IntegerField()
    fullname = forms.CharField(max_length=50)
    email = forms.EmailField()

    MIN_LENGTH = 4

    class Meta:
        model = CustomUser
        fields = ["email", "country_code", "phone", "password", "fullname"]

    def clean_phone_number(self):
        phone = self.data.get("phone")
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                _("Another user with this phone number already exists")
            )
        return phone

    def clean_email(self):
        email = self.data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email addresses must be unique.")
        return email

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data["password"])
        print("Saving user with country_code", user.country_code)
        user.save()
        return user


# ------------ ----- LOGIN FORM PART ---------------------


class LoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ["phone", "password"]


# ------------ ----- ADDRESS FORM PART ---------------------

# ADDRESS FORM
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "fullname",
            "phone",
            "email",
            "house",
            "area",
            "trade",
            "city",
            "pinCode",
            "state",
            "delTime",
        ]
        labels = {
            "house": "Flat, House no., Building, Company, Apartment",
            "trade": "Trademark / Landmark",
            "city": "Town / City",
            "state": "State / Province / Region",
            "area": "Area, Colony, Street, Sector, Village",
            "delTime": "delivery Time",
        }

        widgets = {
            "fullname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter fullname"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "10-digit mobile number without prefixes",
                },
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter Email"},
            ),
            "house": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "eg:- flat no:- 105"},
            ),
            "area": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "eg:- area / colony no- 708",
                },
            ),
            "trade": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "eg:- Near playgorund"},
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter City"},
            ),
            "pinCode": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "eg:- 3320601 "},
            ),
            "state": forms.Select(
                attrs={"class": "form-control", "placeholder": ""},
            ),
            "delTime": forms.Select(
                attrs={"class": "form-control", "placeholder": ""},
            ),
        }
