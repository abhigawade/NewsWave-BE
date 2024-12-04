# Create your models here.
from django.db import models
from authentication.models import User
from article.models import Article

class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_articles')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')  # Prevents duplicate saves of the same article by a user

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"
