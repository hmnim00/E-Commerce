from auctions.models import Bid, Comment, Listing, User, Watchlist
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)