from rest_framework import serializers
from authors.models import CustomUser


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password', 'is_active']
        
    def save(self):
        user = CustomUser(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
        )
        user.set_password(self.validated_data['password'])
        user.is_active = False
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']
