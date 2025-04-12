from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CreateListingForm
from .models import AuctionListing, Bid, Comment

User = get_user_model()


def index(request):
    active_listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return redirect("index")

    return render(request, "auctions/register.html")


def listing_view(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    current_bid = listing.bids.order_by('-bid_amount').first()
    current_price = current_bid.bid_amount if current_bid else listing.starting_bid
    top_bidder = current_bid.bidder.username if current_bid else None
    comments = listing.comments.all().order_by('-commented_at')
    error = None

    if request.method == "POST":
        if "bid_amount" in request.POST:
            try:
                bid_amount = float(request.POST.get("bid_amount"))
                if bid_amount > float(current_price):
                    Bid.objects.create(
                        listing=listing,
                        bidder=request.user,
                        bid_amount=bid_amount
                    )
                    return redirect("listing", listing_id=listing.id)
                else:
                    error = "Your bid must be higher than the current price."
            except (TypeError, ValueError):
                error = "Invalid bid amount."

        elif "comment_text" in request.POST:
            comment_text = request.POST.get("comment_text")
            if comment_text.strip():
                Comment.objects.create(
                    listing=listing,
                    commenter=request.user,
                    comment=comment_text
                )
                return redirect("listing", listing_id=listing.id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": current_price,
        "top_bidder": top_bidder,
        "comments": comments,
        "error": error
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            return redirect("index")
    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)

    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    return redirect("listing", listing_id=listing.id)


@login_required
def watchlist_view(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)

    if request.user == listing.created_by:
        listing.is_active = False
        listing.save()

    return redirect("listing", listing_id=listing.id)
