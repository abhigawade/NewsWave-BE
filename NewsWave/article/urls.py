from django.urls import path, include
from .views import ArticleViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]