from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser

from .utils import get_unique_slug


class Artist(AbstractUser):
    """A website user who can post and collect artworks."""
    # https://www.smashingmagazine.com/2020/02/django-highlights-user-models-authentication/
    bio = models.TextField(blank=True)
    slug = models.SlugField(null=False, unique=True)
    location = models.CharField(max_length=100, blank=True)
    pronouns = models.IntegerField(
        choices=(
            (1, "they/them"),
            (2, "he/him"),
            (3, "she/her")
        ),
        default=1
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'username', 'slug')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/artists/{self.slug}"

    def __str__(self):
        return self.username


class Tag(models.Model):
    """An organizational tag applied to an artwork."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return '#' + self.name

    def get_absolute_url(self):
        return f"/tags/{self.slug}"


class Artwork(models.Model):
    """A single work of art and its metadata."""
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=False, unique=True)
    caption = models.TextField(blank=True)
    image = models.ImageField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    votes = models.ManyToManyField(Artist, related_name='likes')

    @property
    def total_votes(self):
        return self.votes.count()

    def __str__(self):
        return "{0.title} by {0.artist.username}".format(self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/art/{self.slug}"


class Collection(models.Model):
    """A collection of many artworks, maintained by an artist."""
    name = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artworks = models.ManyToManyField(Artwork)
    slug = models.SlugField(null=False, unique=True)
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return "{0.name}, curated by {0.artist.username}".format(self)

    def get_absolute_url(self):
        return f"/collections/{self.slug}"