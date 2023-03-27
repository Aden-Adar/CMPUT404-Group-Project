from rest_framework import serializers
from authors.models import *
from rest_framework.reverse import reverse


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']

    def save(self):
        request = self.context.get('request')
        id = str(uuid.uuid4())
        user = CustomUser(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
            id=id,
            type="author",
            host=request.META.get("HTTP_HOST"),
            url=reverse("author-detail", kwargs = {"id": id}, request=request),
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']
