from rest_framework import serializers
from rest_framework.reverse import reverse
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
    type = serializers.SerializerMethodField(read_only=True)
    parent_comment_id = serializers.IntegerField(write_only=True, required=False)
    author = serializers.SerializerMethodField(read_only=True)
    published = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = Comments
        fields = [
            'type',
            'author',
            'comment',
            'content_type',
            'published',
            'id', # come back to this once author is finished
            'comment_id',
            'post',
            'parent_comment_id'
        ]

    def get_author(self, obj):
        return obj.user.id

    def get_type(self, obj):
        return "comment"

    def get_published(self, obj):
        return obj.published.isoformat()

    def get_id(self, obj):
        return "URL WILL BE HERE SOON"

    def create(self, validated_data):
        try:
            parent_comment_id = validated_data.pop("parent_comment_id")
        except KeyError: # private_post_viewer was not passed
            obj = super().create(validated_data)
            return obj
        else:
            parent_comment = Comments.objects.all().filter(comment_id=parent_comment_id).first()
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
    private_post_viewer = serializers.IntegerField(write_only=True, required=False)
    type = serializers.SerializerMethodField(read_only=True)
    source = serializers.SerializerMethodField(read_only=True)
    origin = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    comments_list = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    published = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Posts
        fields = [
            'type',
            "title",
            'id', # come back to this once author is finished
            'source',
            'origin',
            'description',
            'content_type',
            "content",
            'author', # need a serializer for author
            'comments',
            "comments_list", # needs to be inside comment_src eventually
            'published',
            'visibility',
            'private_post_viewer',
            "unlisted",
            "post_id"
        ]

    def get_type(self, obj):
        return "post"
    
    def get_id(self, obj):
        return "URL WILL BE HERE SOON"
    
    def get_source(self, obj):
        return self.context.get('request').META.get('HTTP_REFERER')
    
    def get_origin(self, obj):
        request = self.context.get('request')
        return reverse("post-detail", kwargs = {"post_id": obj.post_id}, request=request)

    def get_author(self, obj):
        return obj.user_id.id

    def get_comments(self, obj):
        request = self.context.get('request')
        return reverse("comments-list", kwargs = {"post_id": obj.post_id}, request=request)
    
    def get_comments_list(self, obj, **kwargs):
        return CommentSerializer(many=True, read_only=True).data # https://docs.djangoproject.com/en/dev/topics/db/queries/#following-relationships-backward

    def get_published(self, obj):
        return obj.published.isoformat()
    
    def create(self, validated_data):
        try:
            private_post_viewer = validated_data.pop("private_post_viewer")
        except KeyError: # viewer_id was not passed
            if validated_data.get('visibility') == 'PRIVATE':
                raise NotAcceptable(detail="Post cannot be set to private without providing the private post viewer id")
            obj = super().create(validated_data)
        else:
            if validated_data.get('visibility') != 'PRIVATE':
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