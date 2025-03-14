
from rest_framework import serializers
from .models import Comments
from authentication.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Comments
        fields = ['id','comment','article','user','reply','created_at','updated_at']
        read_only_fields = ('user','created_at','updated_at')
        