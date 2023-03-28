from django import forms
from django.core.exceptions import ValidationError  

from authors.models import CustomUser
# https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model/


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", 'password')
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Passwords do not match.')
        else:
            if not password1:
                raise ValidationError('Please enter a password.')
            else:
                raise ValidationError('Please confirm your password.')
        return password2
    
    def save(self, commit=True):        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        
    def clean_password(self):
        return self.initial['password']

