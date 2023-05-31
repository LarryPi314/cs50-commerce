from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, auctionListing, bids, watchList, comments


def index(request):
    return render(request, "auctions/index.html", {
        "auctionListings": auctionListing.objects.all()
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
        
def post_listing(request, name):
    if request.method == "POST":
        new_post = auctionListing(origin = request.user, startingBid = request.POST["startingBid"], title = request.POST["title"], description = request.POST["description"], imgLink = request.POST["imgurl"], category = request.POST["category"], isClosed = False)
        new_post.save()
        return render(request, "auctions/displaylisting.html", {
            "listingBids": bids.objects.filter(listingOn = new_post),
            "auctionListing": new_post
        })
    return render(request, "auctions/postlisting.html")

def display_listing(request, identifier):
    listing = auctionListing.objects.get(pk = identifier)
    if request.method == "POST":
        listing.isClosed = True
        listing.save()
    return render(request, "auctions/displaylisting.html", {
        "listingBids": bids.objects.filter(listingOn = listing),
        "auctionListing": listing,
        "Comments": comments.objects.filter(listingOn = listing)
    })

def watchlist(request, name):
    if request.method == "POST":
        if watchList.objects.filter(origin = request.user, listingOn = auctionListing.objects.get(pk=int(request.POST["wl"]))).exists():
            return render(request, "auctions/watchlist.html", {
                "auctionListings": watchList.objects.filter(origin=request.user),
                "message": "Error: already added to watchlist."
            })
        new_watchlist = watchList(origin = request.user, listingOn = auctionListing.objects.get(pk=int(request.POST["wl"])))
        new_watchlist.save()
        
    return render(request, "auctions/watchlist.html", {
        "auctionListings": watchList.objects.filter(origin=request.user)
    })

def place_bid(request):
    listing = auctionListing.objects.get(pk=int(request.POST["pb"]))
    listing.leaderName = request.user.username
    listing.save()
    is_valid = True
    if int(request.POST["bidVal"]) < listing.startingBid: 
        is_valid = False
    for bid in bids.objects.filter(listingOn = listing):
        if int(request.POST["bidVal"]) < bid.bidVal:
            is_valid = False
    if is_valid:
        new_bid = bids(listingOn = listing, bidder = request.user, bidVal = int(request.POST["bidVal"]))
        new_bid.save()
        return render(request, "auctions/displaylisting.html", {
            "listingBids": bids.objects.filter(listingOn = listing),
            "auctionListing": listing,
            "Comments": comments.objects.filter(listingOn = listing)
        })
    else: 
        return render(request, "auctions/displaylisting.html", {
            "listingBids": bids.objects.filter(listingOn = listing),
            "auctionListing": listing,
            "Comments": comments.objects.filter(listingOn = listing),
            "message": "Bid not valid, you must bid higher than the existing bid values."
        })

def post_comment(request):
    listing = auctionListing.objects.get(pk=int(request.POST["listing"]))
    new_comment = comments(origin=request.user, listingOn=listing, content=request.POST["content"])
    new_comment.save()
    return render(request, "auctions/displaylisting.html", {
        "listingBids": bids.objects.filter(listingOn = listing),
        "auctionListing": listing, 
        "Comments": comments.objects.filter(listingOn = listing)
    })

def display_categories(request):
    distinct_values = auctionListing.objects.values('category').distinct()
    return render(request, "auctions/display_categories.html", {
        "distinct_values": distinct_values
    })

def cat_listings(request, cat):
    return render(request, "auctions/catlistings.html", {
        "auctionListings": auctionListing.objects.filter(category=cat),
        "category": cat
    })



