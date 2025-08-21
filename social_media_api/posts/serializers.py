from rest_framework import serializers
from .models import Post, Comment
from accounts.models import CustomUser # Import your custom user model

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model to represent the author of a post or comment.
    """
    profile_picture = serializers.ImageField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_picture']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    # The author field is a nested serializer to show user details, not just the ID.
    author = CustomUserSerializer(read_only=True)
    
    # We can also add a field to represent the comments on this post.
    comments = serializers.SerializerMethodField()

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
            'comments'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_comments(self, obj):
        """
        Custom method to get all comments for a post.
        Note: This is an example. For large projects, this can be slow.
        """
        # We need to import the CommentSerializer here to avoid circular imports.
        # This is a common pattern for related data.
        from posts.serializers import CommentSerializer
        comments = obj.comments.all().order_by('created_at')
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    # The author field is a nested serializer to show user details.
    author = CustomUserSerializer(read_only=True)
    
    # post = serializers.HiddenField(default=None) # A hidden field for API creation
    # or
    # post = serializers.IntegerField(write_only=True) # or a simple integer field

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']