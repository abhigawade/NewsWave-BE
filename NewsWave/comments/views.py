from django.shortcuts import render
from .models import Comments
from .serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from article.models import Article


# Create your views here.

class CommentsViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    def create(self, request):
        article_id = request.data.get('article')
        article = Article.objects.get(id=article_id)
        if not article:
            return Response({'msg': 'Article is required'}, status=status.HTTP_400_BAD_REQUEST)
        comment_data = CommentSerializer(data=request.data)
        if comment_data.is_valid():
            comment_data.save(user=request.user, article=article)
            return Response({'msg': 'Comment Added Successfully'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Failed to add comment'}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        comment = Comments.objects.get(Q(id=pk) & Q(user_id=request.user.id))
        if not comment:
            return Response({'msg': 'You cannot delete others comment'}, status=status.HTTP_400_BAD_REQUEST)
        comment.delete()
        return Response({'msg': 'Comment deleted Successfully'}, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk):
        comment = Comments.objects.get(Q(id=pk) & Q(user_id=request.user.id))
        comment_data = CommentSerializer(comment,data=request.data,partial=True)
        if comment_data.is_valid():
            comment_data.save()
            return Response({'msg': 'Comment Updated Successfully'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Failed to Update comment'}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        article_id = request.query_params.get('article_id')  # Get article_id from request parameters
        if not article_id:
            return Response({'msg': 'Article ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Comments.objects.filter(article_id=article_id).order_by('-created_at')
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
