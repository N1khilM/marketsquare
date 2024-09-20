import re
from django import forms

from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = (
            'title', 'brand', 'model', 'description', 'price', 
            'color', 'condition', 'stock', 'category', 'image'
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'condition': forms.RadioSelect(),  # Optionally using radio buttons for 'new'/'used'
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Image file size may not exceed 5MB.')
        return image

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock <= 0:
            raise forms.ValidationError('Stock must be greater than zero.')
        return stock