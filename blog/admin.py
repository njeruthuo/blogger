from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'status', 'publish']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['commentator', 'body', 'active', 'created']
    list_editable = ['active']
    list_filter = ['commentator', 'active', 'created']
    search_fields = ['commentator']
