from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post

User = get_user_model()

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    # можно так
    # author = serializers.StringRelatedField()
    author = serializers.ReadOnlyField(source='author.username')

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
    user = serializers.SlugRelatedField(slug_field='username',
                                        queryset=User.objects.all(),
                                        default=(
                                            serializers.CurrentUserDefault())
                                        )
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['following', 'user'],
                message='Вы уже подписаны на данного автора')
        ]

    def validate(self, data):
        if (self.context['request'].method == 'POST'
                and data['user'] == data['following']):
            raise serializers.ValidationError(('Нельзя подписаться'
                                               ' на самого себя'))
        return data
