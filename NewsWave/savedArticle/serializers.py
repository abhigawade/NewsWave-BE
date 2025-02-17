from rest_framework import serializers
from .models import SavedArticle
from article.serializers import ArticleSerializer

class SavedArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)
    class Meta:
        model = SavedArticle
        fields  = ('id', 'user', 'article', 'saved_at')
        read_only_fields = ('id', 'saved_at')