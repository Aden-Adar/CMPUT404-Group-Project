from django import forms
from django.core.exceptions import ValidationError  

from authors.models import CustomUser
# https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model/


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", 'password')
    
    def clean_password2(self):
        password = self.cleaned_data['password']

        if not password:
            raise ValidationError('Please enter a password.')
        return
    
    def save(self, commit=True):        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'github')
        

