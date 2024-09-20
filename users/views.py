from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from marketsquare.models import Listing, LikedListing
from .forms import UserForm, ProfileForm, LocationForm 
from .forms import CustomUserCreationForm, OTPForm  # Import the custom form



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, f'An error occured trying to login.')
        else:
            messages.error(request, f'An error occured trying to login.')
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    return render(request, 'views/login.html', {'login_form': login_form})


@login_required
def logout_view(request):
    #ask user to please not logout with emotion
    logout(request)
    return redirect('main')

from .utils import generate_otp
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        register_form = CustomUserCreationForm()  # Use the custom form here
        return render(request, 'views/register.html', {'register_form': register_form})

    def post(self, request):
        try:
            register_form = CustomUserCreationForm(request.POST)  # Use the custom form here
            if register_form.is_valid():
                # Save user but don't activate yet
                user = register_form.save(commit=False)
                user.is_active = False
                user.save()

                # Generate and store OTP in session
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['user_id'] = user.id
                request.session['otp_expiry'] = str(timezone.now() + timedelta(minutes=5))


                # Send OTP via email
                send_mail(
                    '[MarketSquare] Your OTP for Registration',
                    f"""
    Hello {user.username},

    Thank you for registering with MarketSquare. Your One-Time Password (OTP) for completing the registration is:

    {otp}

    Please use this OTP to complete your registration process. If you did not request this OTP, please ignore this email.

    Best regards,
    The MarketSquare Team
    """,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, 'OTP has been sent to your email.')
                return redirect('verify_otp')  # Redirect to OTP verification page
            else:
                messages.error(request, 'Please correct the errors below.')
        except IntegrityError:
            messages.error(request, 'An error occurred. Please try again.')
            
        return render(request, 'views/register.html', {'register_form': register_form})
    


from django.contrib.auth.models import User
    # OTP Verification View
class OTPVerificationView(View):
    def get(self, request):
        form = OTPForm()
        return render(request, 'views/verify_otp.html', {'form': form})

    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            session_otp = request.session.get('otp')
            user_id = request.session.get('user_id')
            otp_expiry = request.session.get('otp_expiry')

            if not session_otp or not user_id or not otp_expiry:
                messages.error(request, 'OTP session has expired. Please register again.')
                return redirect('register')

            if timezone.now() > timezone.datetime.fromisoformat(otp_expiry):
                messages.error(request, 'OTP has expired. Please try registering again.')
                return redirect('register')

            # Check if the OTP has expired
            if timezone.now() > timezone.datetime.fromisoformat(otp_expiry):
                user = User.objects.get(id=user_id)
                if not user.is_active:
                    user.delete()  # Delete the unverified user if OTP expired
                messages.error(request, 'OTP has expired. Your registration has been canceled.')
                return redirect('register')

            if entered_otp == str(session_otp):
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()

                # Clear the OTP session
                del request.session['otp']
                del request.session['user_id']
                del request.session['otp_expiry']

                login(request, user)
                messages.success(request, 'Registration successful and OTP verified!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        return render(request, 'views/verify_otp.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_liked_listings = LikedListing.objects.filter(
            profile=request.user.profile).all()
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        
        if request.user.profile.location:
            location_form = LocationForm(instance=request.user.profile.location)
        else:
            location_form = LocationForm()
        
        return render(request, 'views/profile.html', {'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'location_form': location_form,
                                                    'user_listings': user_listings,
                                                    'user_liked_listings': user_liked_listings, })

    def post(self, request):
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_liked_listings = LikedListing.objects.filter(
            profile=request.user.profile).all()
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        location_form = LocationForm(
            request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error Updating Profile!')
        return render(request, 'views/profile.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'location_form': location_form,
                                                      'user_listings': user_listings,
                                                      'user_liked_listings': user_liked_listings, })