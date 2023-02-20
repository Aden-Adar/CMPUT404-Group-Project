from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  


User = settings.AUTH_USER_MODEL

class UserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    username = forms.CharField(label='Username', max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True, help_text='Required. 8 characters or more.')
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True, help_text='Enter the same password as before, for verification.')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username
    
    def clean_password2(self):
        if len(self.cleaned_data['password1']) < 8:
            raise ValidationError('Password must be 8 characters or more.')
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('Passwords do not match.')
        return password2
    
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'], 
            self.cleaned_data['password1'])
        return user

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'is_active', 'is_staff', 'is_superuser')
    
    def clean_password(self):
        return self.initial['password']