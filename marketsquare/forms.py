import re
from django import forms

from .models import Listing


from django import forms

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = (
            'title', 'brand', 'model', 'description', 'price', 'discount', 
            'color', 'condition', 'stock', 'category', 'image'
        )

        CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('accessories', 'Accessories'),
        ('smartphones', 'Smartphones'),
        ('shoes', 'Shoes'),
        ('gaming console', 'Gaming Console'),
        ('television', 'Television'),
        ('laptops', 'Laptops'),
        ('watches', 'Watches'),
        ('furniture', 'Furniture'),
        ('footwear', 'Footwear'),
        ('books', 'Books'),
        ('musical instruments', 'Musical Instruments'),
        ('sports equipment', 'Sports Equipment'),
        ('home appliances', 'Home Appliances'),
        ('others','Others'),

    ]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter product title', 'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Brand (optional)', 'class': 'form-control'}),
            'model': forms.TextInput(attrs={'placeholder': 'Enter product model', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Enter a detailed description', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price in USD', 'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'placeholder': 'Optional discount', 'class': 'form-control'}),
            'color': forms.TextInput(attrs={'placeholder': 'Product color', 'class': 'form-control'}),
            'condition': forms.RadioSelect(choices=Listing.CONDITION_CHOICES, attrs={'class': 'form-check-input'}),  
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            # 'category': forms.Select(attrs={'class': 'form-select'}),  
            'category': forms.Select(choices=CATEGORY_CHOICES, attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        price = self.cleaned_data.get('price')
        if discount and price and discount >= price:
            raise forms.ValidationError('Discount cannot be greater than or equal to the price.')
        return discount

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Image file size may not exceed 5MB.')
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError('Only .png, .jpg, and .jpeg formats are allowed.')
        return image

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock <= 0:
            raise forms.ValidationError('Stock must be greater than zero.')
        return stock

    def clean_category(self):
        category = self.cleaned_data.get('category')
        # Use the choices defined in your model for validation
        valid_categories = [choice[0] for choice in Listing.CATEGORY_CHOICES]

        if category and category not in valid_categories:
            raise forms.ValidationError(f'{category} is not a valid category.')
        
        return category

