from django.urls import path
from .views import CommentViewSet, FollowUser, LikeViewSet, PostComments, PostViewSet, UserFeed, UserRegistration, UserLogin

urlpatterns = [
    # User authentication endpoints
    path('api/users/register/', UserRegistration.as_view(), name='user-registration'),
    path('api/users/login/', UserLogin.as_view(), name='user-login'),

    # Post-related endpoints
    path('api/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list-create'),
    path('api/posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='post-detail'),
    path('api/posts/<int:pk>/like/', LikeViewSet.as_view({'post': 'create'}), name='post-like'),
    path('api/posts/<int:pk>/comment/', CommentViewSet.as_view({'post': 'create'}), name='post-comment'),

    # User-related endpoints
    path('api/users/follow/', FollowUser.as_view(), name='follow-user'),
    path('api/users/feed/', UserFeed.as_view(), name='user-feed'),

    # Comments related endpoints
    path('api/posts/<int:post_id>/comments/', PostComments.as_view(), name='post-comments'),
]
