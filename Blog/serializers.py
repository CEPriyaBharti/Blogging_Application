from rest_framework import serializers
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('author',)

    def get_likes(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"  
        read_only_fields = ('author','post')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ('author','post')