from django.shortcuts import render
from .models import SavedArticle
from .serializers import SavedArticleSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from article.models import Article

# Create your views here.

class savedArticleViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = SavedArticle.objects.filter(user=request.user)
        serializer = SavedArticleSerializer(queryset, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK )
    
    def create(self, request):
        article_id = request.data.get('article_id')
        if not article_id:
            return Response({"error": "Article ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        article  = get_object_or_404(Article, id = article_id)
        
        # Check if the article is already saved
        saved_article, created = SavedArticle.objects.get_or_create(user=request.user, article=article)

        if not created:
            return Response({"message": "Article already saved"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Article saved successfully"}, status=status.HTTP_201_CREATED)
        

    def update(self, request, pk=None):
        return Response({"error": "Method Not Allowed"}, status=405)

    def partial_update(self, request, pk=None):
        return Response({"error": "Method Not Allowed"}, status=405)

    def destroy(self, request, pk=None):
        saved_article = get_object_or_404(SavedArticle, id=pk, user=request.user)
        saved_article.delete()
        return Response(
            {"message": "Saved article deleted successfully"},
            status=status.HTTP_200_OK
        )