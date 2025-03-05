from django.contrib import admin
from .models import Comments

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id','comment','article','user','reply','created_at','updated_at']
    list_filter = ['article','user']

admin.site.register(Comments, CommentsAdmin)