from django.contrib import admin
from .models import Article
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):    
    list_display = ('title', 'published_at', 'source', 'url', 'author', 'description', 'url_to_image', 'categories')
    search_fields = ('title', 'content', 'source', 'author', 'description')
    list_filter = ('published_at', 'source', 'author', 'categories')
    
    
