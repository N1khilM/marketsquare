from importlib import reload
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail


from .models import LikedListing, Listing
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter


def main_view(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "views/main.html", {"name": "Marketplace"})


@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(
        profile=request.user.profile).values_list('listing')
    liked_listings_ids = [l[0] for l in user_liked_listings]
    context = {
        'listing_filter': listing_filter,
        'liked_listings_ids': liked_listings_ids,
    }
    return render(request, "views/home.html", context)


@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, )
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(
                    request, f'{listing.model} Listing Posted Successfully!')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(
                request, 'An error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html', {'listing_form': listing_form, 'location_form': location_form, })


@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request, 'views/listing.html', {'listing': listing, })
    except Exception as e:
        messages.error(request, f'Invalid UID {id} was provided for listing.')
        return redirect('home')


@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':

            if 'delete' in request.POST:
                listing.delete()
                messages.success(request, f'Listing {id} deleted successfully!')
                return redirect('home')


            listing_form = ListingForm(
                request.POST, request.FILES, instance=listing)
            location_form = LocationForm(
                request.POST, instance=listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(
                    request, f'An error occured while trying to edit the listing.')
                return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
            context = {
                'location_form': location_form,
                'listing_form': listing_form
            }
            return render(request, 'views/edit.html', context)
    except Exception as e:
        print(e)
        messages.error(
            request, f'An error occured while trying to access the edit page.')
        return redirect('home')


@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)

    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created,
    })


@login_required
def inquire_listing_using_email(request, id):
    """Inquire a listing using email."""
    listing = get_object_or_404(Listing, id=id)
    try:
        
        emailSubject = f'{request.user.username} is interested in {listing.model}'
        emailMessage = (f'Dear {listing.seller.user.username},\n\n'
                        f'We hope this message finds you well. We are pleased to inform you that {request.user.username} has expressed interest in your {listing.model} listing on Marketsquare.\n\n'
                        f'They can be reached at {request.user.email}' + (f' or by phone at {request.user.profile.phone_number}' if request.user.profile.phone_number else '') + ' for further inquiries and communication regarding the listing.\n\n'
                        f'Thank you for using Marketsquare, and we wish you success with your transaction.\n\n'
                        f'Best regards,\n'
                        f'The Marketsquare Team')
        send_mail(emailSubject, emailMessage, 'marketsquareteam@gmail.com',
                  [listing.seller.user.email, ], fail_silently=False)
        return JsonResponse({
            "success": True,
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success": False,
            "info": e,
            })


# unauthorised admin
def not_authorized(request):
    return render(request, 'views/not_authorized.html')