from django.contrib import admin
from .models import SavedArticle
# Register your models here.

@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'saved_at')
    search_fields = ('user', 'article')