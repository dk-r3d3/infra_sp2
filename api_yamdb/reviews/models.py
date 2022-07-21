from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    email = models.EmailField(unique=True, max_length=254)
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=USER_ROLES,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.USER

    def __str__(self):
        return self.role == self.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_registration'
            )
        ]


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} - {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        'Оценка',
        validators=(MinValueValidator(1, message='Минимальное значение 1'),
                    MaxValueValidator(10, message='Максимальное значение 10'))
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий к отзыву'
