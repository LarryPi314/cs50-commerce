from django.contrib.auth.models import AbstractUser
from django.db import models

#post auction listings: user <-> listing 1 to many
#place bids on listings: user <-> listing many to many

#add listings to watchlist: watchlist (user) <-> listing many to many

#comments (on auction listing)
#auction categories

class User(AbstractUser):
    pass

class auctionListing(models.Model):
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    startingBid = models.IntegerField()
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    imgLink = models.CharField(max_length=500, null=True)
    category = models.CharField(max_length=64, null=True)



class bids(models.Model):
    listingOn = models.ForeignKey(auctionListing, on_delete=models.CASCADE, related_name="users")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usersbids")
    bidVal = models.IntegerField()
    

class watchList(models.Model):
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wl")
    listingOn = models.ForeignKey(auctionListing, on_delete = models.CASCADE, related_name="wlpeopple")


class comments(models.Model):
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pplcomments")
    listingOn = models.ForeignKey(auctionListing, on_delete = models.CASCADE, related_name="itemcomments")
    