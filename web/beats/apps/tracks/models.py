"""
Models for Tracks and Genre data
"""
from django.db import models


class Genre(models.Model):
    """ Model for Genre data"""
    # Genre Choices
    # First value represents how its stored in db
    # Second value is what is human readable version 
    GENRE_CHOICES = (
        ('unknown', 'Unknown'),
        ('house', 'House'),
        ('tech_house', 'Tech House'),
        ('deep_house', 'Deep House')
    )

    is_active = models.BooleanField(default=True)
    name = models.CharField(
        choices=GENRE_CHOICES, default='unknown', max_length=255)

    @property
    def is_cool(self):
        """ Returns whether genre is cool or not """
        if self.name == 2:
            return True
        return False


class Track(models.Model):
    """ Model for Track data"""
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    release_date = models.DateTimeField()
    is_purchasable = models.BooleanField(default=False)
    is_available_for_mix = models.BooleanField(default=False)
    title = models.CharField("Title of track", max_length=255)
    genre = models.ForeignKey(Genre, related_name='genre')
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
