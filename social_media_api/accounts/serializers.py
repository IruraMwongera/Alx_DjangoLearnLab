# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate # Don't forget to import this

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # This field will show the number of followers
    followers_count = serializers.SerializerMethodField()
    # This field will show the number of users this user is following
    following_count = serializers.SerializerMethodField()
    # A boolean field to check if the requesting user is following this user
    is_followed_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'bio', 
            'profile_picture', 
            'followers_count', 
            'following_count',
            'is_followed_by_current_user'
        ]
        read_only_fields = ['username', 'email']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        # The 'following' related_name is defined in your CustomUser model
        return obj.following.count()
    
    def get_is_followed_by_current_user(self, obj):
        # This checks if the user making the request is in the obj's followers list
        request_user = self.context.get('request').user
        if request_user.is_authenticated:
            return request_user in obj.followers.all()
        return False


class UserProfileSerializer(serializers.ModelSerializer):
    """
    A simple serializer for displaying a user's profile, including their follower and following counts.
    """
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers_count', 'following_count']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Make sure 'authenticate' is imported
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()