from rest_framework import serializers
from listings.models import Listing, Spec, ListingPhoto
from users.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'seller_type',
            'bio',
            'propic',
            'location'
        )
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'email',
            'first_name',
            'last_name',
            'userprofile'
        )

class SpecSerializer(serializers.ModelSerializer):
    # user = serializers.RelatedField()
    # category = serializers.RelatedField()

    class Meta:
        model = Spec
        fields = (
            'id',
            'name',
            'value',
            'listing'
        ) 

class ListingPhotoSerializer(serializers.ModelSerializer):
    # user = serializers.RelatedField()
    # category = serializers.RelatedField()

    class Meta:
        model = ListingPhoto
        fields = (
            'id',
            'url',
            'key',
            'order',
            'listing'
        ) 

class ListingSerializer(serializers.ModelSerializer):
    spec_set = SpecSerializer(required=False, many=True)
    listingphoto_set = ListingPhotoSerializer(required=False, many=True)
    user = UserSerializer()
    # category = serializers.RelatedField()

    class Meta:
        model = Listing