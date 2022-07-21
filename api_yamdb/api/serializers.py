"""High level support for doing this and that."""
from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, Category, Genre, Title, Review, Comment


class SignUpSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Такой email уже используется!')
        ]
    )

    class Meta:
        """High level support for doing this and that."""

        model = User
        fields = ('email', 'username')

    @staticmethod
    def validate_username(value):
        """High level support for doing this and that."""
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!'
            )
        return value

    def create(self, validated_data):
        """High level support for doing this and that."""
        user = User.objects.create(**validated_data)
        return user


class TokenSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        """High level support for doing this and that."""

        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    class Meta:
        """High level support for doing this and that."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class MeSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    role = serializers.CharField(read_only=True)

    class Meta:
        """High level support for doing this and that."""

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CategorySerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    class Meta:
        """High level support for doing this and that."""

        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    class Meta:
        """High level support for doing this and that."""

        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(source='reviews__score__avg',
                                      read_only=True)

    class Meta:
        """High level support for doing this and that."""

        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        """High level support for doing this and that."""

        model = Title
        fields = '__all__'

    @staticmethod
    def validate_year(value):
        """High level support for doing this and that."""
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год выхода не может быть больше текущего!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='name',
                                         read_only=True)

    class Meta:
        """High level support for doing this and that."""

        model = Review
        fields = '__all__'

    @staticmethod
    def validate_score(value):
        """High level support for doing this and that."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10!'
            )
        return value

    def validate(self, data):
        """High level support for doing this and that."""
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)

        review = Review.objects.select_related(
            'author', 'title').filter(title=title, author=author)

        if review.exists() and request.method == 'POST':
            raise serializers.ValidationError(
                'Вы уже писали отзыв к данному произведению!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """High level support for doing this and that."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.SlugRelatedField(slug_field='text',
                                          read_only=True)

    class Meta:
        """High level support for doing this and that."""

        model = Comment
        fields = '__all__'
