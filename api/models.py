from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds an extra 'name' field 
    """
    # Optional full name for the user
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username

class Stock(models.Model):
    """ Model representing a stock in the market. """

    # The stock ticker symbol (e.g., AAPL, GOOGL).
    symbol = models.CharField(max_length=10, unique=True)

    # The full name of the company.
    name = models.CharField(max_length=255)
    
    # The current price of the stock.
    price = models.DecimalField(max_digits=12, decimal_places=2)

    # The timestamp of the last price update, automatically sets to current datetime whenever object is saved.
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class Watchlist(models.Model):
    """ Model representing a user's stock watchlist. """
    
    # The user who owns this watchlist.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # The stock being watched.
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
    # The date and time when the stock was added to the watchlist.
    added_at = models.DateTimeField(auto_now_add=True)

    # Ensure that a user cannot add the same stock to their watchlist more than once.
    class Meta:
        unique_together = ('user', 'stock')

    def __str__(self):
        return f"{self.user.username} watches {self.stock.symbol}"