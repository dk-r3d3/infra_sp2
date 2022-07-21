"""High level support for doing this and that."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, CategoryViewSet, GenreViewSet,
    ReviewViewSet, CommentViewSet, TitleViewSet, signup, token
)

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', signup),
    path('token/', token)
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router.urls))
]
