from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

User = settings.AUTH_USER_MODEL

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'github']
    list_filter = ['username', 'github']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('github',)}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    search_fields = ['username', 'github']
    

admin.site.register(CustomUser, CustomUserAdmin)