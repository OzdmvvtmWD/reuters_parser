
import json
import requests
from load_django import *  
from parser_app.models import *
from django.utils.dateparse import parse_datetime


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.reuters.com/sustainability/shareholder-activism/",
    "Origin": "https://www.reuters.com"
}

size = 100
offset = 0

url = f'https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?query=%7B%22arc-site%22%3A%22reuters%22%2C%22fetch_type%22%3A%22collection%22%2C%22offset%22%3A{offset}%2C%22requestId%22%3A2%2C%22section_id%22%3A%22%2Fsustainability%2Fshareholder-activism%2F%22%2C%22size%22%3A%22{size}%22%2C%22uri%22%3A%22%2Fsustainability%2Fshareholder-activism%2F%22%2C%22website%22%3A%22reuters%22%7D&d=318&mxId=00000000&_website=reuters'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    articles = data['result']['articles']
    print(len(articles))

    for item in articles:
        thumb_data = item.get("thumbnail", {})
        thumbnail = None
        if thumb_data and thumb_data.get("url"):
            thumbnail, _ = Thumbnail.objects.get_or_create(
                url=thumb_data["url"],
                defaults={
                    "alt_text": thumb_data.get("alt_text"),
                    "caption": thumb_data.get("caption"),
                    "width": thumb_data.get("width"),
                    "height": thumb_data.get("height"),
                    "resizer_url": thumb_data.get("resizer_url"),
                    "subtitle": thumb_data.get("subtitle"),
                    "updated_at": parse_datetime(thumb_data.get("updated_at")) if thumb_data.get("updated_at") else None,
                }
            )

        article, created = Article.objects.update_or_create(
            article_id=item["id"],
            defaults={
                "title": item["title"],
                "basic_headline": item.get("basic_headline"),
                "description": item.get("description"),
                "canonical_url": "https://www.reuters.com" + item["canonical_url"],
                "website": item["website"],
                "published_time": parse_datetime(item["published_time"]),
                "updated_time": parse_datetime(item["updated_time"]),
                "display_time": parse_datetime(item["display_time"]),
                "read_minutes": item.get("read_minutes"),
                "word_count": item.get("word_count"),
                "article_type": item.get("article_type"),
                "content_code": item.get("content_code"),
                "source_name": item.get("source", {}).get("name", "Reuters"),
                "company_rics": item.get("company_rics"),
                "thumbnail": thumbnail,
                "primary_tag_text": item.get("primary_tag", {}).get("text"),
                "primary_tag_url": "https://www.reuters.com" + item.get("primary_tag", {}).get("topic_url", ""),
                "kicker_name": item.get("kicker", {}).get("name"),
                "kicker_path": "https://www.reuters.com" + item.get("kicker", {}).get("path", ""),
            }
        )

        article.authors.clear()
        for author_data in item.get("authors", []):
            author, _ = Author.objects.get_or_create(
                name=author_data.get("name", "Reuters"),
                defaults={
                    "email": author_data.get("id") if "@" in author_data.get("id", "") else None,
                    "company": author_data.get("company", "Reuters"),
                    "byline": author_data.get("byline"),
                    "topic_url": "https://www.reuters.com" + author_data.get("topic_url", ""),
                    "thumbnail_url": author_data.get("thumbnail", {}).get("url"),
                }
            )
            article.authors.add(author)

        article.save()

else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
