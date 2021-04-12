# TODO:  Напишите свой вариант
from typing import List
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Post, Group, Follow
from .serializers import GroupSerializer, PostSerializer, CommentSerializer, FollowSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        if group_id:
            return get_list_or_404(Post, group=group_id)
        return Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post_id = self.request.parser_context['kwargs'].get('post_id')
        post = get_object_or_404(Post, id=post_id)
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post_id = self.request.parser_context['kwargs'].get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username',] 

    def perform_create(self, serializer):
        username = self.request.POST.get('user')
        following_name = self.request.POST.get('following')
        user = get_object_or_404(User, username=username)
        following = get_object_or_404(User, username=following_name)
        return serializer.save(user=user, following=following)
    
    def get_queryset(self):
        user = self.request.user
        return user.following.all()
