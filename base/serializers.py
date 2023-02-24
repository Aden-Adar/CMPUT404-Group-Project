from rest_framework import serializers
from .models import *
from rest_framework.exceptions import NotAcceptable, ValidationError

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

class PrivatePostViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivatePostViewer
        fields = [
            'post_id',
            'viewer_id'
        ]

    # def create(self, validated_data):
    #     print("Validated Data (last): ", validated_data)
    #     print(validated_data)
    #     PrivatePostViewer.objects.create(post_id=validated_data['post_id'], viewer_id=validated_data['viewer_id'] )

    #     return validated_data

class PostSerializer(serializers.ModelSerializer):
    private_post_viewer = serializers.IntegerField(write_only=True)
    class Meta:
        model = Posts
        fields = [
            'pk',
            'post_visibility',
            'user_id',
            'published',
            'private_post_viewer',
            'content_type',
            "title",
            "content",
            "unlisted"
        ]


    def create(self, validated_data):

        private_post_viewer = validated_data.pop("private_post_viewer")
        obj = super().create(validated_data)

        private_post_viewer_serializer = PrivatePostViewerSerializer(data=[{
                "post_id": obj.id,
                "viewer_id" : private_post_viewer
            }]
            , many=True)

        if validated_data.get('post_visibility') == 'V':
            if CustomUser.objects.filter(id=private_post_viewer).exists():
                if private_post_viewer_serializer.is_valid():
                    private_post_viewer_serializer.save()
                else:
                    raise ValidationError()
            else:
                raise NotAcceptable(detail="User does not exist")
        else:
            NotAcceptable(detail="Visibility must be set to private when including viewer id")


        return obj

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'title',
            'description',
            'image'
        ]