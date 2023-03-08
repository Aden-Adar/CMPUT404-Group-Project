from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authors.models import CustomUser
from .forms import UserChangeForm, UserCreationForm


class CustomUserAdmin(UserAdmin):
    form = UserCreationForm
    add_form = UserChangeForm
    list_display = ('username', 'github')
    list_filter = ('github',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('github',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', )
    

admin.site.register(CustomUser, CustomUserAdmin)