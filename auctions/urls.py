from auctions.views import makeOffer
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new-listing', views.newListing, name='newListing'),
    path('create', views.createListing, name='createListing'),
    path('listing/<int:listingId>', views.listing, name='listing'),
    path('add/<int:listingId>', views.addToWatchlist, name='addToWatchlist'),
    path('remove/<int:listingId>', views.removeFromWatchlist, name='removeFromWatchlist'),
    path('watchlist/<str:username>', views.watchlist, name='watchlist'),
    path('categories', views.categories, name='categories'),
    path('category/<str:category>', views.category, name='category'),
    path('submitOffer/<int:listingId>', views.makeOffer, name='makeOffer'),
    path('closed-listings', views.closedListings, name='closedListings'),
    path('close-listing/<int:listingId>', views.closeListing, name='closeListing'),
    path('comment/<int:listingId>', views.comment, name='comment')
]
