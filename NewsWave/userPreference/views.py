from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from userPreference.models import UserPreference
from userPreference.serializers import UserPreferenceSerializer

class UserPreferenceView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPreferenceSerializer
    
    def create(self, request):
        if UserPreference.objects.filter(user=request.user).exists():
            return Response({"error": "User already has preferences."}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        
        if "preferred_topics" in data:
            data["preferred_topics"] = [topic.lower() for topic in data["preferred_topics"]]
            
        if "preferred_sources" in data:
            data["preferred_sources"] = [source.lower() for source in data["preferred_sources"]]
        
        serializer = UserPreferenceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Preferences created successfully."},
                status=status.HTTP_201_CREATED,
            )

    def retrieve(self, request):
        try:
            # Fetch preferences for the authenticated user
            preferences = UserPreference.objects.get(user=request.user)
            serializer = UserPreferenceSerializer(preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserPreference.DoesNotExist:
            return Response({"error": "Preferences not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        data = request.data.copy()
        
        if "preferred_topics" in data:
            data["preferred_topics"] = [topic.lower() for topic in data["preferred_topics"]]
            
        if "preferred_sources" in data:
            data["preferred_sources"] = [source.lower() for source in data["preferred_sources"]]
        
        serializer = UserPreferenceSerializer(preferences, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Preferences updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
