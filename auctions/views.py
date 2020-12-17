from auctions.forms import ListingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import request
from django.http import response
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Bid, Comment, Listing, User, Watchlist


def index(request):
    listings = Listing.objects.filter(status=True)
    categories = Listing.objects.raw(
        'SELECT * FROM auctions_listing GROUP BY category HAVING COUNT(*)>=1')
    empty = False
    try:
        w = Watchlist.objects.filter(user=request.user)
        total = len(w)
    except:
        total = None
    return render(request, 'auctions/index.html', {
        'listings': listings,
        'total': total,
        'empty': empty,
        'categories': categories
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


@login_required(login_url='login')
def newListing(request):
    try:
        watch = Watchlist.objects.filter(user=request.user)
        total = len(watch)
    except:
        total = None

    return render(request, 'auctions/new-listing.html', {
        'total': total
    })


@login_required
def createListing(request):
    owner = Listing(owner=request.user)
    form = ListingForm()

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=owner)

        if form.is_valid():
            form.instance.currentBid = form.cleaned_data['initialBid']
            form.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, 'auctions/new-listing.html')

    context = {'form': form, }
    return render(request, 'auctions/new-listing.html', context)


def listing(request, listingId):
    try:
        item = Listing.objects.get(id=listingId)
    except:
        return redirect('index')
    try:
        comments = Comment.objects.filter(listingId=listingId)
        allComm = len(comments)
    except:
        comments = None
        allComm = None
    if request.user:
        try:
            if Watchlist.objects.get(user=request.user, listingId=listingId):
                added = True
        except:
            added = False

        try:
            listing = Listing.objects.get(id=listingId)
            if listing.owner == request.user:
                seller = True
            else:
                seller = False

        except:
            return redirect('index')
    else:
        added = False
        seller = False
    try:
        w = Watchlist.objects.filter(user=request.user)
        total = len(w)
    except:
        total = None

    return render(request, 'auctions/listing.html', {
        'listing': item,
        'added': added,
        'seller': seller,
        'total': total,
        'error': request.COOKIES.get('error'),
        'success': request.COOKIES.get('success'),
        'comments': comments,
        'allComm': allComm
    })


@login_required(login_url='login')
def addToWatchlist(request, listingId):
    if request.user.username:
        w = Watchlist()
        w.user = request.user.username
        w.listingId = listingId
        w.save()
        return redirect('listing', listingId=listingId)
    else:
        return redirect('index')


@login_required(login_url='login')
def removeFromWatchlist(request, listingId):
    if request.user:
        try:
            w = Watchlist.objects.get(
                user=request.user.username, listingId=listingId)
            w.delete()
            return redirect('listing', listingId=listingId)
        except:
            return redirect('listing', listingId=listingId)
    else:
        return redirect('index')


@login_required(login_url='login')
def watchlist(request, username):
    if request.user:
        try:
            w = Watchlist.objects.filter(user=username)
            items = []
            for i in w:
                items.append(Listing.objects.filter(id=i.listingId))
            try:
                w = Watchlist.objects.filter(user=request.user)
                total = len(w)
            except:
                total = None
            return render(request, 'auctions/watchlist.html', {
                'items': items,
                'total': total
            })
        except:
            try:
                w = Watchlist.objects.filter(user=request.user)
                total = len(w)
            except:
                total = None
            return render(request, 'auctions/watchlist.html', {
                'items': None,
                'total': total
            })
    else:
        return redirect('index')


@login_required(login_url='login')
def makeOffer(request, listingId):
    listing = Listing.objects.get(id=listingId)
    price = listing.currentBid
    if request.method == 'POST':
        offer = int(request.POST.get('offer'))
        if offer > price:
            item = Listing.objects.get(id=listingId)
            item.currentBid = offer
            item.save()

            try:
                if Bid.objects.filter(id=listingId):
                    bid = Bid.objects.filter(id=listingId)
                    bid.delete()
                newBid = Bid()
                newBid.user = request.user
                newBid.listingId = item.listingId
                newBid.bid = offer
                newBid.save()

            except:
                newBid = Bid()
                newBid.user = request.user
                newBid.listingId = listingId
                newBid.bid = offer
                newBid.save()

            response = redirect('listing', listingId=listingId)
            response.set_cookie(
                'success', 'Your bid has been succesfully added!', max_age=3)
            return response
        else:
            response = redirect('listing', listingId=listingId)
            response.set_cookie(
                'error', 'Your bid must be greater than the current one', max_age=3)
            return response
    else:
        return redirect('index')


@login_required(login_url='login')
def closeListing(request, listingId):
    try:
        listing = Listing.objects.get(id=listingId)
    except:
        return redirect('index')

    try:
        listing.status = False
        listing.winner = Bid.objects.filter(listingId=listingId).last().user
        listing.save()
    except:
        listing.owner = request.user
        listing.save()
    try:
        if Watchlist.objects.filter(listingId=listingId):
            w = Watchlist.objects.filter(listingId=listingId)
            w.delete()
        else:
            pass
    except:
        pass

    return HttpResponseRedirect(reverse('listing', args=[listingId]))


@login_required(login_url='login')
def closedListings(request):
    items = Listing.objects.filter(status=False)
    empty = False
    try:
        w = Watchlist.objects.filter(user=request.user)
        total = len(w)
    except:
        total = None
    return render(request, 'auctions/closed-listings.html', {
        'listings': items,
        'total': total,
        'empty': empty
    })


@login_required(login_url='login')
def comment(request, listingId):
    try:
        listing = Listing.objects.get(id=listingId)
        if request.method == 'POST':
            newComment = Comment()
            newComment.comment = request.POST.get('comment')
            newComment.user = request.user
            newComment.listingId = listing
            newComment.save()
            return HttpResponseRedirect(reverse('listing', args=[listingId]))
        else:
            return redirect('listing')
    except:
        return redirect('index')


@login_required(login_url='login')
def deleteListing(request, listingId):
    listing = Listing.objects.get(id = listingId)
    listing.delete()
    
    return HttpResponseRedirect(reverse("index"))