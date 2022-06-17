from django.contrib import admin

from api_yamdb.settings import VALUE_DISPLAY

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'role'
    )
    search_fields = ('username',)
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('slug',)
    list_filter = ('slug',)
    empty_value_display = VALUE_DISPLAY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('case_name',)
    search_fields = ('name',)
    list_filter = ('genre', 'category')
    empty_value_display = VALUE_DISPLAY

    def case_name(self, obj):
        return ('%s %s %s %s' % (obj.name, obj.year, obj.genre, obj.category))


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'title', 'pub_date', 'score')
    search_fields = ('author', 'title')
    list_filter = ('author', 'title')
    empty_value_display = VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date')
    search_fields = ('author', 'review')
    list_filter = ('author', 'review')
    empty_value_display = VALUE_DISPLAY
