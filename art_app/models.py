from django.db import models
from django.contrib.auth.models import AbstractUser

class Artist(AbstractUser):
    """A website user who can post and collect artworks."""
    # https://www.smashingmagazine.com/2020/02/django-highlights-user-models-authentication/
    bio = models.TextField()
    location = models.CharField(max_length = 100, blank=True)
    pronouns = models.IntegerField(
        choices=(
            (1, "they/them"),
            (2, "he/him"),
            (3, "she/her")
        ),
        default=1
    )

class Tag(models.Model):
    """An organizational tag applied to an artwork."""
    name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length = 200, primary_key=True)

class Artwork(models.Model):
    """A single work of art and its metadata."""
    title = models.CharField(max_length=200)
    caption = models.TextField()
    image = models.ImageField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    votes = models.IntegerField()

class Collection(models.Model):
    """A collection of many artworks, maintained by an artist."""
    name = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artworks = models.ManyToManyField(Artwork)
    tags = models.ManyToManyField(Tag)