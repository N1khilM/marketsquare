import uuid
from django.db import models


from users.models import Profile, Location
from .utils import user_listing_path
# Create your models here.
from.models import Profile, Location


class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    
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
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('under_review', 'Under Review'),
    ]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)  # General product type (e.g., electronics, clothing)
    brand = models.CharField(max_length=24, null=True)  # Optional, remove if not applicable
    model = models.CharField(max_length=64,)  # Product model name
    description = models.TextField()  # Detailed product description

    price = models.DecimalField(max_digits=10, decimal_places=2,default="0")  # Price of the product
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional discount

    color = models.CharField(max_length=24,)  # Color of the product
    
    location = models.OneToOneField(
        Location, on_delete=models.SET_NULL, null=True) #location inherited
    image = models.ImageField(upload_to=user_listing_path)
    
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES, default='new')  # New or used condition
    
    stock = models.PositiveIntegerField(default=1)  # Stock quantity
    
    # category = models.CharField(max_length=50,choices=CATEGORY_CHOICES, null=True, blank=True)  # Optional category
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True) 
    
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='active')  # Active, sold, or under review



    def __str__(self):
        return f'{self.seller.user.username}\'s Product Listing - {self.model}'




class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.listing.model} listing liked by {self.profile.user.username}'