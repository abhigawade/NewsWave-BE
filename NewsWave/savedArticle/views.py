from django.shortcuts import render
from .models import SavedArticle
from .serializers import SavedArticleSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class savedArticleViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedArticleSerializer
    
    def get_queryset(self, request):
        return SavedArticle.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user= self.request.user)