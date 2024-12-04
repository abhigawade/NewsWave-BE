from django.contrib import admin
from userPreference.models import UserPreference
# Register your models here.

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_topics', 'preferred_sources')
    search_fields = ('user', 'preferred_topics', 'preferred_sources')
    list_filter = ('user',)