from django.conf import settings
from django.urls import path

from .views import adminpanel

urlpatterns = [
    path('', adminpanel, name='adminpanel'),
]

