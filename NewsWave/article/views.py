from django.shortcuts import render
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Article.objects.all().order_by('-published_at')
        category = request.query_params.get('category', None)
        search_query = request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(categories__contains=[category])
            
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(description__icontains=search_query)
            
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        return Response({"error": "Method Not Allowed"}, status=405)
    
    def create(self, request):
        return Response({"error": "Method Not Allowed"}, status=405)

    def update(self, request, pk=None):
        return Response({"error": "Method Not Allowed"}, status=405)

    def partial_update(self, request, pk=None):
        return Response({"error": "Method Not Allowed"}, status=405)

    def destroy(self, request, pk=None):
        return Response({"error": "Method Not Allowed"}, status=405)
