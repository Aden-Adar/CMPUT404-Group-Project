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

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'title',
            'description',
            'image'
        ]

class CommentSerializer(serializers.ModelSerializer):
    parent_comment_id = serializers.IntegerField(write_only=True, required=False)
    user = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Comments
        fields = [
            'type',
            'id',
            'user',
            'post',
            'parent_comment_id',
            'content_type',
            'published',
            'content'
        ]

    def get_user(self, obj):
        return obj.user.id

    def get_type(self, obj):
        return "comment"

    def create(self, validated_data):
        try:
            parent_comment_id = validated_data.pop("parent_comment_id")
        except KeyError: # private_post_viewer was not passed
            obj = super().create(validated_data)
            return obj
        else:
            parent_comment = Comments.objects.all().filter(pk=parent_comment_id).first()
            if parent_comment:
                validated_data["parent_comment_id"] = parent_comment
                obj = super().create(validated_data)
                return obj
            else:
                raise NotAcceptable(detail="Parent comment id does not exist")


    """   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent_comment_id = models.IntegerField(default = (-1))
    content_type = models.CharField(max_length=200, choices=ContentType.choices, default=ContentType.PLAIN)
    published = models.TimeField(auto_now_add=True)
    content = models.TextField(max_length=301,editable=True) """

class PostSerializer(serializers.ModelSerializer):
    comments_set = CommentSerializer(many=True, read_only=True) # https://docs.djangoproject.com/en/dev/topics/db/queries/#following-relationships-backward

    private_post_viewer = serializers.IntegerField(write_only=True, required=False)
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
            "unlisted",
            "comments_set"
        ]


    def create(self, validated_data):
        try:
            private_post_viewer = validated_data.pop("private_post_viewer")
        except KeyError: # viewer_id was not passed
            if validated_data.get('post_visibility') == 'V':
                raise NotAcceptable(detail="Post cannot be set to private without providing the private post viewer id")
            obj = super().create(validated_data)
        else:
            if validated_data.get('post_visibility') != 'V':
                raise NotAcceptable(detail="Private post viewer id should only be included for private posts")
            if CustomUser.objects.filter(id=private_post_viewer).exists():
                obj = super().create(validated_data)
                private_post_viewer_serializer = PrivatePostViewerSerializer(data=[{
                        "post_id": obj.id,
                        "viewer_id" : private_post_viewer
                    }]
                    , many=True)
                if private_post_viewer_serializer.is_valid():
                    private_post_viewer_serializer.save()
                else:
                    obj.delete()
                    raise ValidationError()
            else:
                raise NotAcceptable(detail="User does not exist")

        return obj