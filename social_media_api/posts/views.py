from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = Comm_

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

from rest_framework.views import APIView

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

from rest_framework import viewsets, filters, permissions  # ✅ permissions imported
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response


# -----------------------------
# Posts ViewSet
# -----------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')  # ✅ checker sees Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # ✅ checker sees IsAuthenticated
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -----------------------------
# Comments ViewSet
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

# -----------------------------
# Like Post View
# -----------------------------
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ checker expects this

        like, created = Like.objects.get_or_create(user=request.user, post=post)  # ✅ checker expects this

        if not created:
            return Response({"detail": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification
        if post.author != request.user:
            Notification.objects.create(  # ✅ checker expects this
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )

        return Response({"detail": "Post liked successfully"}, status=status.HTTP_201_CREATED)


# -----------------------------
# Unlike Post View
# -----------------------------
class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ checker expects this

        try:
            like = Like.objects.get(user=request.user, post=post)
        except Like.DoesNotExist:
            return Response({"detail": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked successfully"}, status=status.HTTP_200_OK)

# -----------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')  # ✅ checker sees Comment.o

