# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserSerializer  # must exist in accounts/serializers.py


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    Includes nested author info, comment count, and like count.
    """
    author = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'content',
            'image',
            'created_at',
            'updated_at',
            'comments_count',
            'likes_count',
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.count() if hasattr(obj, "comments") else 0

    def get_likes_count(self, obj):
        return obj.likes.count() if hasattr(obj, "likes") else 0


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Includes nested author details.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    Includes nested user details.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = [
            'id',
            'user',
            'post',
            'created_at',
        ]
        read_only_fields = ['user', 'created_at']
