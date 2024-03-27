from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment, Like, User, Post, Follower
from .serializers import CommentSerializer, LikeSerializer, UserSerializer, PostSerializer, FollowerSerializer


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(TokenObtainPairView):
    pass

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FollowUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        follower = request.user
        user_id_to_follow = request.data.get('user_id')
        try:
            user_to_follow = User.objects.get(id=user_id_to_follow)
            if not Follower.objects.filter(user=user_to_follow, follower=follower).exists():
                Follower.objects.create(user=user_to_follow, follower=follower)
                return Response({'message': 'User followed successfully'})
            else:
                return Response({'message': 'User already followed'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'})

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserFeed(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followed_users = Follower.objects.filter(follower=request.user).values_list('user', flat=True)
        posts = Post.objects.filter(author__in=followed_users)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostComments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)