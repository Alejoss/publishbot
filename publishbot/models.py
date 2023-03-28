from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField
from taggit.managers import TaggableManager


class Publication(models.Model):

    PUBLICATION_TYPE_CHOICES = (
        ("text", 'Text'),
        ("image", 'Image'),
        ("video", 'Video'),
        ("url", 'URL'),
    )

    text = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='publications/images', blank=True, null=True)
    video = models.FileField(upload_to='publications/videos', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    tags = TaggableManager()
    priority = models.SmallIntegerField(default=0)
    canceled = models.BooleanField(default=False)
    publication_type = models.CharField(max_length=10, choices=PUBLICATION_TYPE_CHOICES, default="text")
    score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.publication_type} - {self.text}"


class Event(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, related_name='events')
    publication_time = models.DateTimeField()
    success = models.BooleanField(default=False)
    network_response = JSONField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    reactions = JSONField(blank=True, null=True)
    published_data = JSONField(blank=True, null=True)
    score_data = JSONField(blank=True, null=True)

    def __str__(self):
        return f'Event for Publication {self.publication_id} at {self.publication_time}'


class Configuration(models.Model):
    antiquity_multiplier = models.SmallIntegerField(default=1)
    content_type_multiplier = models.SmallIntegerField(default=1)
    priority_multiplier = models.SmallIntegerField(default=1)
    cycle_days = models.SmallIntegerField(default=7)
    publications_per_week = models.SmallIntegerField(default=7)

    def __str__(self):
        return f'Configuration #{self.pk}'

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
