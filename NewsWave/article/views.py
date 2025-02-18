from django.shortcuts import render
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from googletrans import Translator
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
    
    

# Article Summary View
class ArticleSummary(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)

        text = article.description

        if not text:
            return Response({"error": "No content available for summarization"}, status=status.HTTP_400_BAD_REQUEST)

        # Use Sumy for summarization
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 5)  # Summarize to 4 sentences

        # Generate summary text
        summary_text = " ".join(str(sentence) for sentence in summary_sentences)
            
        return JsonResponse({"title": article.title,"summary": summary_text}, status=status.HTTP_200_OK)
    
    
# Article Translate View
class ArticleTranslate(APIView):
    def get(self, request, pk):
        
        target_language = request.GET.get('language', 'en')
        
        article = get_object_or_404(Article, id=pk)
        
        # Translate the article title and description
        translator = Translator()
        try:
            translated_title = translator.translate(article.title, dest=target_language).text
            translated_description = translator.translate(article.description, dest=target_language).text
            
            return JsonResponse({"title": translated_title, "description": translated_description}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Translation failed"}, status=status.HTTP_400_BAD_REQUEST)