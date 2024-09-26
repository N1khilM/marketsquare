# /middleware.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.deprecation import MiddlewareMixin

class AdminAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if user is trying to access the admin site
        if request.path.startswith('/admin/'):
            # Check if the user is authenticated and is staff
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect('not_authorized')  # Redirect to a 'not authorized' page
