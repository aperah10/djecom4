from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


from .models import *
from .forms import *

# Register your models here.

# Custom Accounts
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "id",
        "phone",
        "fullname",
        "email",
        "is_staff",
        "password",
    )
    list_filter = (
        "email",
        "phone",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("phone", "password", "email", "fullname")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "fullname",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("phone",)
    ordering = ("id",)


admin.site.register(CustomUser, CustomUserAdmin)


# CUSTOMER ADMIN / PROFILE
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "uplod", "gender", "email", "pic", "fullname")


# ADDRESS ADMIN
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "uplod", "city", "house", "trade", "pinCode", "state")
