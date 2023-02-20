from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        """
        Create and saves the User with the given email and password.
        """
        if not username:
            raise ValueError(_('The Username needs to be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.active = False
        user.save()
        return user
    
    def create_staffuser(self, username, password, **extra_fields):
        """
        Create and save a staff user with the given email and password.
        """
        staff_user = self.create_user(username, password, **extra_fields)
        staff_user.is_staff = True
        staff_user.save()
        return staff_user
    
    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """

        super_user = self.create_user(username, password, **extra_fields)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save()
        return super_user
    
