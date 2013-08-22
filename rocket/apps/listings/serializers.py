from rest_framework import serializers
from listings.models import Listing

class ListingSerializer(serializers.ModelSerializer):
    # user = serializers.RelatedField()
    # category = serializers.RelatedField()

    class Meta:
        model = Listing
        fields = (
            'id',
            'title', 
            'price', 
            'description', 
            'last_modified', 
            'create_date',             
            'listing_type', 
            'location', 
            'category', 
            'status',
            'listingphoto_set', 
            'spec_set',
        ) 