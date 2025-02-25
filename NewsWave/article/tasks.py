import json
import requests
from celery import shared_task
from .models import Article
from datetime import datetime
from django.conf import settings

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string



# api_key = settings.NEWS_API_KEY

# NEWS_API_URL = ''   # The Newsapi

# @shared_task
# def get_articles():
#     """Fetch news from an external API and store it in the database."""
#     # params = {
#     #     "apiKey": NEWS_API_URL,
#     #     "pageSize": 2,
#     # }

#     response = requests.get(NEWS_API_URL)
    
#     print(response.status_code)

#     if response.status_code == 200:
#         news_data = response.json()
#         for article in news_data.get("data", []):
#             # Convert publishedAt string to datetime object
#             published_at = datetime.strptime(article["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

#             # Save only if the article URL is unique
#             Article.objects.get_or_create(
#                 url=article["url"],
#                 defaults={
#                     "source": article["source"],  
#                     "title": article["title"],
#                     "description": article.get("description", ""),
#                     "url_to_image": article.get("image_url", ""),
#                     "published_at": published_at,
#                     "content": article.get("snippet", ""),
#                     "categories": article.get("categories", []),
#                 },
#             )
#             print("------------------Done ------------------")
#     return "News articles fetched and stored successfully."



NEWS_API_URL = "https://api.worldnewsapi.com/top-news?source-country=in&language=en&date=2025-01-07"
API_KEY = settings.NEWS_API_KEY

nltk.download("punkt")
nltk.download("stopwords")

CATEGORIES_KEYWORDS = {
    "general": [
        "news", "trending", "update", "daily", "breaking", "report", "latest",
        "current events", "headlines", "important", "media", "press", "international",
        "global", "local", "coverage", "top stories", "happenings", "today"
    ],
    "politics": [
        "election", "government", "senate", "president", "parliament", "policy",
        "democracy", "minister", "congress", "laws", "vote", "diplomacy", "legislation",
        "political", "campaign", "rights", "opposition", "governance"
    ],
    
    "sports": [
        "football", "soccer", "basketball", "tennis", "olympics", "FIFA", 
        "cricket", "badminton", "athletics", "hockey", "golf", "marathon",
        "boxing", "wrestling", "NBA", "Premier League", "World Cup", "tournament"
    ],
    
    "technology": [
        "AI", "artificial intelligence", "tech", "software", "gadgets", "Google", 
        "Microsoft", "innovation", "blockchain", "cybersecurity", "cloud computing",
        "5G", "robotics", "IoT", "virtual reality", "data science", "programming",
        "startup", "machine learning", "automation", "space", "Elon Musk"
    ],
    
    "health": [
        "covid", "health", "vaccine", "medicine", "hospital", "doctor", "wellness", 
        "mental health", "fitness", "nutrition", "cancer", "treatment", "heart disease", 
        "yoga", "workout", "pandemic", "therapy", "diet", "flu", "hygiene", "physiotherapy"
    ],
    
    "business": [
        "stock", "market", "finance", "investment", "economy", "entrepreneur", "startup", 
        "mergers", "banking", "real estate", "cryptocurrency", "trading", "corporate", 
        "shares", "interest rate", "inflation", "GDP", "mutual funds", "business growth"
    ],
    
    "entertainment": [
        "movie", "music", "celebrity", "Hollywood", "Bollywood", "Netflix", "actor", 
        "actress", "award", "festival", "box office", "theater", "series", "showbiz", 
        "director", "cinema", "Grammy", "Oscar", "concert", "streaming", "drama"
    ],
    
    "food": [
        "recipe", "cooking", "cuisine", "restaurant", "chef", "healthy eating", "vegan", 
        "vegetarian", "fast food", "dessert", "spices", "street food", "breakfast", 
        "lunch", "dinner", "snack", "drink", "organic", "diet", "nutrition", "protein"
    ],
    
    "travel": [
        "vacation", "tourism", "adventure", "flights", "hotel", "resort", "beach", 
        "mountains", "road trip", "hiking", "camping", "backpacking", "passport", 
        "visa", "airlines", "cruise", "holiday", "tour", "destinations", "sightseeing"
    ],
    
    "india": [
        "Delhi", "Mumbai", "Kolkata", "Chennai", "Hyderabad", "Bangalore", "Pune", 
        "Indian economy", "Modi", "elections", "RBI", "Indian culture", "Taj Mahal", 
        "Ayodhya", "Indian festival", "Diwali", "Holi", "Republic Day", "Independence Day",
        "Ganga", "Bollywood", "Indian cricket", "IPL", "Yoga", "Ayurveda", "Make in India",
        "ISRO", "Chandrayaan", "Indian startup", "Indian cuisine", "Indian heritage"
    ],

    "trends": [
        "viral", "trending", "social media", "TikTok", "Instagram", "Twitter", "YouTube", 
        "meme", "challenge", "influencer", "NFT", "crypto", "Metaverse", "AI revolution", 
        "streaming wars", "celebrity gossip", "fashion trends", "climate change", 
        "global events", "breaking news", "hot topics", "latest news", "controversy"
    ]
}




def categorize_article_nltk(title, content):
    """Categorize article using NLTK-based keyword matching."""
    text = title + " " + content  
    words = word_tokenize(text.lower())  # Tokenize & convert to lowercase
    words = [word for word in words if word not in stopwords.words("english") and word not in string.punctuation]

    found_categories = set()
    for category, keywords in CATEGORIES_KEYWORDS.items():
        if any(keyword.lower() in words for keyword in keywords):
            found_categories.add(category)

    return list(found_categories) if found_categories else ["general"]



@shared_task
def get_articles():
    """Fetch news from an external API and store it in the database."""
    headers = {"x-api-key": API_KEY}
    response = requests.get(NEWS_API_URL, headers=headers)

    if response.status_code == 200:
        news_data = response.json()

        if "top_news" in news_data and news_data["top_news"]:
            articles = news_data["top_news"][0].get("news", [])

            for article in articles:
                published_at = datetime.strptime(article["publish_date"], "%Y-%m-%d %H:%M:%S")
                title = article["title"][:200]
                content = article.get("text", "")

                # Categorize article using NLTK
                categories = categorize_article_nltk(title, content)

                article_obj, created = Article.objects.get_or_create(
                    url=article["url"],
                    defaults={
                        "source": article.get("authors", ["Unknown"])[0],
                        "title": title,
                        "description": article.get("summary", ""),
                        "url_to_image": article.get("image", ""),
                        "published_at": published_at,
                        "content": content,
                        "categories": categories,
                    },
                )
                
                if created:
                    article_obj.save() 
                    print(f"Article {title} added successfully!")
                else:
                    print(f"Article already exists in the database.")

    return "News articles fetched and stored successfully."