from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import savedArticleViewset

router = DefaultRouter()
router.register(r'saved-articles', savedArticleViewset, basename='saved-articles')

urlpatterns = [
    path('', include(router.urls)),
]
