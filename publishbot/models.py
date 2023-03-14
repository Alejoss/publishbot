from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='tweet_images', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text}"
