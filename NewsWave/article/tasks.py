import requests
from celery import shared_task
from .models import Article
from datetime import datetime
from django.conf import settings


# NEWS_API_URL = "https://newsapi.org/v2/everything?q=india&apiKey=21025d1583d44ba6a0575f90b9d68ac0"
# API_KEY = "21025d1583d44ba6a0575f90b9d68ac0"

# api_key = settings.NEWS_API_KEY

NEWS_API_URL = 'https://api.thenewsapi.com/v1/news/all?api_token=8NcN3P8dAMwDYFMhQ8TRYdueD5qsOsMOrfv6PXJE&language=en&limit=3'



@shared_task
def get_articles():
    """Fetch news from an external API and store it in the database."""
    # params = {
    #     "apiKey": NEWS_API_URL,
    #     "pageSize": 2,
    # }

    response = requests.get(NEWS_API_URL)
    
    print(response.status_code)
    print('****************************************************')

    if response.status_code == 200:
        news_data = response.json()
        for article in news_data.get("data", []):
            # Convert publishedAt string to datetime object
            published_at = datetime.strptime(article["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

            # Save only if the article URL is unique
            Article.objects.get_or_create(
                url=article["url"],
                defaults={
                    "source": article["source"],  
                    "title": article["title"],
                    "description": article.get("description", ""),
                    "url_to_image": article.get("image_url", ""),
                    "published_at": published_at,
                    "content": article.get("snippet", ""),
                    "categories": article.get("categories", []),
                },
            )
            print("------------------Done ------------------")
    return "News articles fetched and stored successfully."
