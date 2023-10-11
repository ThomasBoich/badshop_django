from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserChangeForm, CustomUserCreationForm
from users.models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'email',
        'first_name',
        'last_name',
        'patronymic',
        'is_staff',
        'is_active',
        'phone',
    )
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'first_name',
            'last_name',
            'patronymic',
            'photo',
            'phone',
        )}),
        ('Permissions', {
            'fields': ('is_superuser', 'ban', 'type', 'is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active',
                'is_superuser',
                'ban',
                'type',
                'first_name',
                'last_name',
                'patronymic',
                'phone',

            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class ProfileAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)