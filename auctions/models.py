from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import math


class User(AbstractUser):
    pass


class Listing(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='seller')
    title = models.CharField(max_length=64)
    description = models.TextField()
    initialBid = models.DecimalField(max_digits=8, decimal_places=2)
    currentBid = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(blank=True, null=True, default='no-image.jpg')
    category = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name='buyer')

    def createdAt(self):
        return self.date.strftime('%d %B %Y')


class Bid(models.Model):
    listingId = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=8, decimal_places=2)


class Comment(models.Model):
    listingId = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def createdAt(self):
        return self.date.strftime('%d %B %Y')
        now = timezone.now()
        dif = now - self.date

        if dif.days == 0 and dif.seconds >= 0 and dif.seconds < 60:
            seconds = dif.seconds
            if seconds == 1:
                return str(seconds) + ' seconds ago'
            else:
                return str(seconds) + ' seconds ago'

        if dif.days == 0 and dif.seconds >= 60 and dif.seconds < 3600:
            minutes = math.floor(dif.seconds/60)
            if minutes == 1:
                return str(minutes) + ' minute ago'
            else:
                return str(minutes) + ' minutes ago'

        if dif.days == 0 and dif.seconds >= 0 and dif.seconds < 86400:
            hours = math.floor(dif.seconds/3600)
            if hours == 1:
                return str(hours) + ' hour ago'
            else:
                return str(hours) + ' hours ago'

        if dif.days >= 1 and dif.days < 30:
            days = dif.days
            if days == 1:
                return str(days) + ' day ago'
            else:
                return str(days) + ' days ago'

        if dif.days >= 30 and dif.days < 365:
            months = math.floor(dif.days/30)
            if months == 1:
                return str(months) + ' month ago'
            else:
                return str(months) + ' months ago'

        if dif.days >= 365:
            years = math.floor(dif.days/365)
            if years == 1:
                return str(years) + ' year ago'
            else:
                return str(years) + ' years ago'


class Watchlist(models.Model):
    listingId = models.IntegerField()
    user = models.CharField(max_length=64)
