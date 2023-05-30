from django.contrib import admin

from .models import User, auctionListing, bids, watchList, comments

# Register your models here.

admin.site.register(User)
admin.site.register(auctionListing)
admin.site.register(bids)
admin.site.register(watchList)
admin.site.register(comments)