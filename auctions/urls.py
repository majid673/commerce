from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_listing, name="create"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("listing/<int:listing_id>/", views.listing_view, name="listing"),  
    path("watchlist/<int:listing_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/", views.watchlist_view, name="watchlist"),
    path("listing/<int:listing_id>/close/", views.close_listing, name="close_listing"),

]


