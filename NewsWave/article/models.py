from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    source = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    published_date = models.DateTimeField()
    language = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    is_translated = models.BooleanField(default=False)
    translation_language = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title