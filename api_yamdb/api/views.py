"""High level support for doing this and that."""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters, permissions, mixins
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category, Genre, Title, Review
from .filters import TitleFilter
from .permissions import (
    IsAdmin, IsAuthor, ReadOnly, IsModerator, IsSuperuser
)
from .serializers import (
    SignUpSerializer, TokenSerializer, UserSerializer, CategorySerializer,
    GenreSerializer, TitleSerializer, MeSerializer, CommentSerializer,
    ReviewSerializer, TitleGetSerializer
)
DOMAIN_NAME = 'yamdb.ru'
EMAIL_NAME = 'userverify'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@action(methods=['post'], detail=False)
def signup(request):
    """High level support for doing this and that."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')

    user = User.objects.get_or_create(username=username, email=email)[0]

    confirmation_code = default_token_generator.make_token(user)
    email_subject = 'Код подтверждения'
    email_message = (f'Привет {user.username}, '
                     f'твой код подтверждения:{confirmation_code}')

    send_mail(subject=email_subject,
              message=email_message,
              from_email=f'{EMAIL_NAME}@{DOMAIN_NAME}',
              recipient_list=[user.email],
              fail_silently=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@action(methods=['post'], detail=False)
def token(request):
    """High level support for doing this and that."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)

    confirmation_code = serializer.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user).access_token
        return Response({'token': token},
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """High level support for doing this and that."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsSuperuser]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def users_me(self, request):
        """High level support for doing this and that."""
        user = request.user
        user = get_object_or_404(User, username=user.username)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """High level support for doing this and that."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """High level support for doing this and that."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """High level support for doing this and that."""

    queryset = Title.objects.annotate(Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdmin | ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """High level support for doing this and that."""
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """High level support for doing this and that."""

    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        (ReadOnly | IsAdmin | IsModerator | IsAuthor)
    ]

    def get_queryset(self):
        """High level support for doing this and that."""
        """High level support for doing this and that."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """High level support for doing this and that."""
        """High level support for doing this and that."""
        author = self.request.user
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """High level support for doing this and that."""

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        (ReadOnly | IsAdmin | IsModerator | IsAuthor)
    ]

    def get_queryset(self):
        """High level support for doing this and that."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """High level support for doing this and that."""
        author = self.request.user
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=author, review=review)
