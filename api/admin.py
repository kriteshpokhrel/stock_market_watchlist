from django.contrib import admin
from .models import Stock, Watchlist

# Register your models here.
admin.site.register(Stock)
admin.site.register(Watchlist)