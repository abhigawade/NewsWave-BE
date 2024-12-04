from rest_framework import serializers
from userPreference.models import UserPreference
from authentication.models import User

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['user', 'preferred_topics', 'preferred_sources']
        read_only_fields = ['user']