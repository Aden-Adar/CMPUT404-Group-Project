from rest_framework import serializers
from .models import *


class CreateAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['username','password']
        
    def save(self):
        user = CustomUser(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']