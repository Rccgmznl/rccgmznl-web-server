from django.core.exceptions import ValidationError
from django.db import models

from django.utils import timezone

class BasicEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    cover_image_url = models.URLField()
    cover_image_alt_text = models.CharField(max_length=255)
    external_url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Basic Event"
        verbose_name_plural = "Basic Events"

class BibleReference(models.Model):
    reference = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.reference

    class Meta:
        verbose_name = "Bible Reference"
        verbose_name_plural = "Bible References"


class HeroImage(models.Model):
    url = models.URLField()
    alt_text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.alt_text

    class Meta:
        verbose_name = "Hero Image"
        verbose_name_plural = "Hero Images"

class WelcomeContent(models.Model):
    text = models.TextField()
    image_url = models.URLField()
    image_alt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = "Welcome Content"
        verbose_name_plural = "Welcome Contents"

class LastestSermon(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    cover_image_url = models.URLField()
    cover_image_alt_text = models.CharField(max_length=255)
    preacher = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    external_url = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Lastest Sermon"
        verbose_name_plural = "Lastest Sermons"

class HeroGallery(models.Model):
    image = models.URLField()
    alt_text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.alt_text

    class Meta:
        verbose_name = "Hero Gallery"
        verbose_name_plural = "Hero Galleries"
