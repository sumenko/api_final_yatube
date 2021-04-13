from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import validators

from .models import Comment, Post, Group, Follow
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # можно так
    # author = serializers.StringRelatedField()
    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='username', default=serializers.CurrentUserDefault())
    # user = serializers.HiddenField(source='user.username', default=serializers.CurrentUserDefault())
    # following = serializers.ReadOnlyField(source='following.username')
    # user = serializers.ReadOnlyField(default=serializers.CurrentUserDefault())

    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())
    
    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]
