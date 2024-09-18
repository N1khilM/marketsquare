from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from marketsquare.models import LikedListing, Listing

# Create your views here.
from importlib import reload
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from marketsquare.models import LikedListing, Listing
from marketsquare.forms import ListingForm
from users.forms import LocationForm
from marketsquare.filters import ListingFilter

from django.shortcuts import render
from django.contrib.auth.models import User
from marketsquare.models import Listing, Location, LikedListing

def adminpanel(request):
    # Gather data
    total_users = User.objects.all()[::-1][:5]
    # total_listings = Listing.objects.all()
    # total_locations = Location.objects.all()
    # total_liked_listings = LikedListing.objects.all()
    location_form=LocationForm()

    # Get the most recent listings
    recent_listings = Listing.objects.order_by('-created_at')[::-1][:5]

    # Pass the data to the template
    context = {
        'Users': total_users,
        # 'total_listings': total_listings,
        # 'total_locations': total_locations,
        # 'total_liked_listings': total_liked_listings,
        'recent_listings': recent_listings,
    }

    return render(request, 'views/adminpanel.html', context)



def usersdetails(request):
    # Gather data
    user=request.id
    total_users = User.objects(id=user.id)
    listings = Listing.objects(id=id)
    profile=User
    # total_locations = Location.objects.all()
    # total_liked_listings = LikedListing.objects.all()

    return render(request,'views/userdetails',listings)
