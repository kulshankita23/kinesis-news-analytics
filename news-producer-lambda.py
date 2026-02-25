
import json
import boto3
import requests
from datetime import datetime

KINESIS_STREAM = "news-stream"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

kinesis = boto3.client("kinesis")

def lambda_handler(event, context):
    response = requests.get(NEWS_API_URL)
    news_data = response.json()

    articles = news_data.get("articles", [])

    for article in articles:
        news_event = {
            "headline": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "timestamp": datetime.utcnow().isoformat(),
            "priority": "HIGH" if "breaking" in (article.get("title") or "").lower() else "LOW"
        }

        kinesis.put_record(
            StreamName=KINESIS_STREAM,
            PartitionKey="news",
            Data=json.dumps(news_event)
        )

    print(f"Sent {len(articles)} articles to Kinesis")
    return {"status": "success"}