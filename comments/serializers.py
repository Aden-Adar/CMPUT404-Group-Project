from rest_framework import serializers
from .models import *
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.reverse import reverse


class CommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    # parent_comment_id = serializers.IntegerField(write_only=True, required=False)
    author = serializers.SerializerMethodField(read_only=True)
    published = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    post = serializers.SerializerMethodField(read_only=True)

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
            # 'parent_comment_id'
        ]

    def get_author(self, obj):
        return obj.user.id

    def get_type(self, obj):
        return "comment"

    def get_published(self, obj):
        return obj.published.isoformat()

    def get_id(self, obj):
        request = self.context.get('request')
        return reverse("comment-detail", kwargs={"author_id" : obj.user_id, "post_id" : obj.post.post_id, "comment_id" : obj.comment_id}, request=request)

    def get_post(self, obj):
        return obj.post.post_id

    def create(self, validated_data):
        obj = super().create(validated_data)
        print(obj.post)
        return obj
        # try:
        #     parent_comment_id = validated_data.pop("parent_comment_id")
        # except KeyError: # private_post_viewer was not passed
        #     print(validated_data)
        #     obj = super().create(validated_data)
        #     return obj
        # else:
        #     parent_comment = Comments.objects.all().filter(comment_id=parent_comment_id).first()
        #     if parent_comment:
        #         validated_data["parent_comment_id"] = parent_comment
        #         obj = super().create(validated_data)
        #         return obj
        #     else:
        #         raise NotAcceptable(detail="Parent comment id does not exist")


    """   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent_comment_id = models.IntegerField(default = (-1))
    content_type = models.CharField(max_length=200, choices=ContentType.choices, default=ContentType.PLAIN)
    published = models.TimeField(auto_now_add=True)
    content = models.TextField(max_length=301,editable=True) """
