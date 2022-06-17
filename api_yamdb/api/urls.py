from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, MeView,
                    ReviewViewSet, TitleViewSet, TokenObtainView,
                    UserModelViewSet, UserRegistrationView)

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserModelViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', UserRegistrationView.as_view()),
    path('v1/auth/token/', TokenObtainView.as_view()),
    path('v1/users/me/', MeView.as_view()),
    path('v1/', include(router_v1.urls)),
]
