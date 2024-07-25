from django.shortcuts import render
from  rest_framework.viewsets import ModelViewSet
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework import permissions





class PostViewset(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeViewset(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)


    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)

class CommentViewset(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
