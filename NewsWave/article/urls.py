from django.urls import path, include
from .views import ArticleViewSet
from rest_framework import routers

from .views import ArticleSummary, ArticleTranslate

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/<int:pk>/', ArticleSummary.as_view(), name='summary'),
    path('translate/<int:pk>/', ArticleTranslate.as_view(), name='translate'),
]