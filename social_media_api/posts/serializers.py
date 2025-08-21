# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.models import CustomUser
from accounts.serializers import UserSerializer  # Ensure this is correctly imported and functional

# -------------------------------------------------------------------
# You should use a single UserSerializer. It's best practice to define it
# once in accounts/serializers.py and import it everywhere else.
# Your code imports it, so we will use it directly.
# The CustomUserSerializer below is a duplicate, so it's removed.
# -------------------------------------------------------------------


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    It includes nested user details, comment count, and like count.
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
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    """
    user = UserSerializer(read_only=True)  # Display user details

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']  # User will be set by the view