from django.conf import settings
from django.contrib import admin

from .models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date',)
    search_fields = ('title', 'score', 'pub_date',)
    list_filter = ('title', 'score', 'pub_date',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date',)
    search_fields = ('review', 'author',)
    list_filter = ('pub_date',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
