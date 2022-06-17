import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from reviews.models import Category, Comment, Genre, Review, Title, User

from .permissions import (AdminOnly, AdminOrReadOnly,
                          AuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TokenSerializer, UserSerializer,
                          UserSignUpSerializer)


class UserRegistrationView(views.APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = str(uuid.uuid4())
            serializer.save(confirmation_code=confirmation_code)
            self.send_confirmation_email(
                serializer.data['email'], confirmation_code
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_confirmation_email(self, email, confirmation_code):
        send_mail(
            subject='Confirmation code',
            message=confirmation_code,
            from_email=settings.AUTH_EMAIL,
            recipient_list=[email]
        )


class TokenObtainView(TokenViewBase):
    serializer_class = TokenSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated, AdminOnly)


class MeView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorModeratorAdminOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorModeratorAdminOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title=title_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AdminOrReadOnly
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AdminOrReadOnly
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        queryset = Title.objects.all()
        genre_slug = self.request.query_params.get('genre')
        if genre_slug is not None:
            genre = Genre.objects.get(slug=genre_slug)
            queryset = queryset.filter(genre=genre)
        category_slug = self.request.query_params.get('category')
        if category_slug is not None:
            category = Category.objects.get(slug=category_slug)
            queryset = queryset.filter(category=category)
        year = self.request.query_params.get('year')
        if year is not None:
            queryset = queryset.filter(year=year)
        name = self.request.query_params.get('name')
        if name is not None:
            queryset.filter(name__startswith=name)
        return queryset
