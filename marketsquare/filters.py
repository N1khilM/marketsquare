import django_filters

from .models import Listing


class ListingFilter(django_filters.FilterSet):

    class Meta:
        model = Listing
        fields = {
            'title': ['icontains'],
        #     'brand': ['exact'],
        #     'model': ['icontains'],
            'color': ['exact'],
            'price': ['gt', 'lt']  # combined gt and lt filters
        }

    