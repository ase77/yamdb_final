from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if not username or not email:
            raise ValueError('User must have username and email')

        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        user = self.create_user(username, email, password, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.role = UserRole.ADMIN
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    ROLES_CHOICES = (
        (UserRole.USER, UserRole.USER),
        (UserRole.MODERATOR, UserRole.MODERATOR),
        (UserRole.ADMIN, UserRole.ADMIN)
    )

    username = models.CharField(
        unique=True, max_length=150
    )
    email = models.EmailField(
        unique=True, max_length=254
    )
    confirmation_code = models.CharField(
        blank=True, max_length=150
    )
    first_name = models.CharField(
        blank=True, max_length=150
    )
    last_name = models.CharField(
        blank=True, max_length=150
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=150, choices=ROLES_CHOICES, default=UserRole.USER
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    @property
    def is_moderator_or_admin(self):
        return self.role in (UserRole.MODERATOR, UserRole.ADMIN)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    rating = models.IntegerField(
        default=None,
        null=True,
        verbose_name='Рейтинг'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(
        validators=(
            MaxValueValidator(10, 'максимальная оценка 10'),
            MinValueValidator(1, 'минимальная оценка 1'),
        ),
        verbose_name='Оценка',
    )

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='one_review_for_title'
            ),
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
