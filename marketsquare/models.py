import uuid
from django.db import models


from users.models import Profile, Location
from .utils import user_listing_path
# Create your models here.
from.models import Profile, Location


class Listing(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)  # General product type (e.g., electronics, clothing)
    brand = models.CharField(max_length=24, null=True)  # Optional, remove if not applicable
    model = models.CharField(max_length=64,)  # Product model name
    description = models.TextField()  # Detailed product description
    price = models.DecimalField(max_digits=10, decimal_places=2,default="0")  # Price of the product
    color = models.CharField(max_length=24,)  # Color of the product
    location = models.OneToOneField(
        Location, on_delete=models.SET_NULL, null=True) #location inherited
    image = models.ImageField(upload_to=user_listing_path)
    
    
    def __str__(self):
        return f'{self.seller.user.username}\'s Product Listing - {self.model}'




class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.listing.model} listing liked by {self.profile.user.username}'