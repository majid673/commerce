from django.contrib import admin
from .models import User
from .models import AuctionListing, Bid, Comment

admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
# Register your models here.
