import datetime

from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import (Category, Comment, Genre, Review, Title, User,
                            UserRole)


class BaseUserSerializer:
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('username "me" is locked')
        return value

    def validate_role(self, value):
        if self.instance and self.instance.role == UserRole.USER:
            return UserRole.USER
        return value


class UserSignUpSerializer(BaseUserSerializer, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']


class UserSerializer(BaseUserSerializer, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]


class TokenSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def validate(self, attrs):
        data = {}
        username = attrs['username']
        confirmation_code = attrs['confirmation_code']

        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound(
                'No user with such username.'
            )

        if self.user.confirmation_code != confirmation_code:
            raise exceptions.ValidationError(
                'No user with such credentials.'
            )

        token = self.get_token(self.user)
        data['token'] = str(token)
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы можете добавить однин отзыв на произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Genre


class StrToDictData(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return {"name": obj.name, "slug": obj.slug}


class TitleSerializer(serializers.ModelSerializer):
    genre = StrToDictData(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = StrToDictData(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if len(reviews) == 0:
            return None
        score_list = [getattr(review, 'score') for review in list(reviews)]
        return round(sum(score_list) / len(score_list))

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if not (0 < value <= current_year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value
