from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', views.CommentViewSet,
                basename='comments')
router.register(r'group', views.GroupViewSet, basename='group')
router.register(r'follow', views.FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router.urls)),
]
