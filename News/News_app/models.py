from django.db import models

class Article(models.Model):
    headline = models.CharField(max_length=200)
    image_url = models.URLField()
    text = models.TextField()
    date = models.TextField()
    time = models.TextField()
    read_more_url = models.URLField()