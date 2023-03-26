from rest_framework import serializers
from authors.models import *
from rest_framework.reverse import reverse


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']
        
    def save(self):
        request = self.context.get('request')
        self.validated_data["id"] = str(uuid.uuid4())
        self.validated_data["type"] = "author"
        self.validated_data["host"] = request.META.get("HTTP_HOST")
        self.validated_data["url"] = reverse("author-detail", kwargs = {"id": self.validated_data["id"]}, request=request)

        # user = CustomUser(
        #     username=self.validated_data['username'],
        #     password=self.validated_data['password'],
        #     id=str(uuid.uuid4()),
        #     type="author",
        #     url=reverse("author-detail", kwargs = {"id": self.validated_data["id"]}, request=request)
        # )
        # user.set_password(self.validated_data['password'])
        # user.save()
        # return user

        obj = super().create(self.validated_data)
        return obj

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']
