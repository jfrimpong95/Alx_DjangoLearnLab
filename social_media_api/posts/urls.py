from .views import FeedView
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls

# Add feed endpoint
urlpatterns += [
    path('feed/', FeedView.as_view(), name='feed')
]

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView

# DRF router for PostViewSet and CommentViewSet
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# Start with router URLs
urlpatterns = router.urls

# Add explicit URLs for feed, like, and unlike
urlpatterns += [
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),     # ✅ checker string
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post') # ✅ checker string
]
