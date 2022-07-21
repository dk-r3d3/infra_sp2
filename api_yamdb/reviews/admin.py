"""High level support for doing this and that."""
from django.contrib import admin
from .models import User, Title, Category, Genre, Comment, Review


class UserAdmin(admin.ModelAdmin):
    """High level support for doing this and that."""

    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )


class TitleAdmin(admin.ModelAdmin):
    """High level support for doing this and that."""

    list_display = (
        'name',
        'year',
        'category',
        'description',
    )


class CategoryAdmin(admin.ModelAdmin):
    """High level support for doing this and that."""

    list_display = (
        'name',
        'slug',
    )


class GenreAdmin(admin.ModelAdmin):
    """High level support for doing this and that."""

    list_display = (
        'name',
        'slug',
    )


class ReviewAdmin(admin.ModelAdmin):
    """High level support for doing this and that."""

    list_display = (
        'title',
        'text',
        'author',
        'score',
    )


class CommentAdmin(admin.ModelAdmin):
    """High level support for doing this and that."""

    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )


ADMINS_LIST = (
    (User, UserAdmin),
    (Title, TitleAdmin),
    (Category, CategoryAdmin),
    (Genre, GenreAdmin),
    (Comment, CommentAdmin),
    (Review, ReviewAdmin)
)

for model, admins in ADMINS_LIST:
    admin.site.register(model, admins)
