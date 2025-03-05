from .views import CommentsViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', CommentsViewset, basename='comments')
urlpatterns = router.urls