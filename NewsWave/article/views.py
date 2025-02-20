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
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)

        text = article.content

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
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        
        target_language = request.GET.get('language', 'en')
        
        article = get_object_or_404(Article, id=pk)
        
        if not article.title:
            return Response({"error": "No title available for translation"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not article.content:
            return Response({"error": "No content available for translation"}, status=status.HTTP_400_BAD_REQUEST)
        
        MAX_TRANSLATION_LENGTH = 5000
        content_text = article.content[:MAX_TRANSLATION_LENGTH]
        
        # Translate the article title and description
        translator = Translator()
        try:
            translated_title = translator.translate(article.title, dest=target_language).text
            translated_content = translator.translate(content_text, dest=target_language).text
            
            return JsonResponse({"title": translated_title, "description": translated_content}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Translation failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)



class ArticleDownload(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="NewsWave.pdf"'

        pdf_canvas = canvas.Canvas(response, pagesize=letter)
        pdf_canvas.setTitle(article.title)

        # Define page width and margins
        page_width, page_height = letter
        left_margin = 50
        right_margin = 50
        max_width = page_width - left_margin - right_margin
        y_position = page_height - 80  # Start below the top margin

        # Add title with wrapping
        pdf_canvas.setFont("Helvetica-Bold", 16)
        title_lines = simpleSplit(article.title, "Helvetica-Bold", 16, max_width)

        for line in title_lines:
            pdf_canvas.drawString(left_margin, y_position, line)
            y_position -= 20  # Move down for each line

        y_position -= 10  # Extra space after title

        # Add Source and Date
        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(left_margin, y_position, f"Source: {article.source}")
        y_position -= 20
        pdf_canvas.drawString(left_margin, y_position, f"Published At: {article.published_at.strftime('%Y-%m-%d')}")
        y_position -= 30  # Space before content

        # Add content with wrapping
        pdf_canvas.setFont("Helvetica", 10)
        content_lines = simpleSplit(article.content, "Helvetica", 10, max_width)

        for line in content_lines:
            if y_position < 50:  # Move to the next page if needed
                pdf_canvas.showPage()
                y_position = page_height - 80  # Reset Y position on new page
                pdf_canvas.setFont("Helvetica", 10)  # Reset font on new page

            pdf_canvas.drawString(left_margin, y_position, line)
            y_position -= 15  # Move down for next line

        pdf_canvas.save()
        return response