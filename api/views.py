from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins
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


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username']        

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return self.request.user.following
