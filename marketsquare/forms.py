import re
from django import forms

from .models import Listing


class ListingForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Listing
        fields = ('title','brand', 'model', 'description',
                  'price', 'color', 'image')