
from rest_framework import serializers
from .models import Comments

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id','comment','article','user','reply','created_at','updated_at']
        read_only_fields = ('user','created_at','updated_at')
        