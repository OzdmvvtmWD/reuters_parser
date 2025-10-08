from django.db import models


class Thumbnail(models.Model):
    url = models.URLField()
    alt_text = models.TextField(null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    resizer_url = models.URLField(null=True, blank=True)
    subtitle = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.url


class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    byline = models.CharField(max_length=255, null=True, blank=True)
    topic_url = models.URLField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    article_id = models.CharField(max_length=255, unique=True)
    title = models.TextField()
    basic_headline = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    canonical_url = models.URLField()
    website = models.CharField(max_length=100)
    published_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    display_time = models.DateTimeField()
    read_minutes = models.IntegerField(null=True, blank=True)
    word_count = models.IntegerField(null=True, blank=True)
    article_type = models.CharField(max_length=100, null=True, blank=True)
    content_code = models.CharField(max_length=100, null=True, blank=True)
    source_name = models.CharField(max_length=100)
    company_rics = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)  

    
    # Allow many articles to share a thumbnail
    thumbnail = models.ForeignKey(Thumbnail, on_delete=models.SET_NULL, null=True, blank=True)
    
    primary_tag_text = models.CharField(max_length=255, null=True, blank=True)
    primary_tag_url = models.URLField(null=True, blank=True)
    kicker_name = models.CharField(max_length=255, null=True, blank=True)
    kicker_path = models.URLField(null=True, blank=True)

    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title
