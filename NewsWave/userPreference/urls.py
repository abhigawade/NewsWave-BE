from django.urls import path
from .views import UserPreferenceView

urlpatterns = [
    path('userPreference/', UserPreferenceView.as_view({'post': 'create', 'get': 'retrieve', 'patch': 'patch'})),
]