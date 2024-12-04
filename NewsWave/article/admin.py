from django.contrib import admin
from .models import Article
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'source', 'url', 'language', 'category', 'is_translated', 'translation_language')
    search_fields = ('title', 'content', 'source', 'language', 'category', 'translation_language')
    list_filter = ('published_date', 'language', 'category', 'is_translated', 'translation_language')