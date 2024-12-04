from rest_framework import serializers
from .models import SavedArticle

class SavedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedArticle
        fields  = ('id', 'user', 'article', 'saved_at')
        read_only_fields = ('id', 'saved_at')