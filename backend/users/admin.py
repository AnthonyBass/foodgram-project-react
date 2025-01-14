from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Follow

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    list_display = [
        "email",
        "username",
        "is_superuser",
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
