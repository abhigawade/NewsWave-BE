from django.db import models

# Create your models here.   
class Article(models.Model):
    source = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    url_to_image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    categories = models.JSONField(default=list, null=True, blank=True)

    
    def __str__(self):
        return self.title