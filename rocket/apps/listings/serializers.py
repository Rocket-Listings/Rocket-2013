from rest_framework import serializers
from listings.models import Listing, Spec, ListingPhoto, Buyer, Message
from users.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime

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

class ListingDetailSerializer(serializers.ModelSerializer):
    spec_set = SpecSerializer(required=False, many=True)
    listingphoto_set = ListingPhotoSerializer(required=False, many=True)
    link = serializers.CharField(source='get_absolute_url', read_only=True)
    user = UserSerializer()
    # category = serializers.RelatedField()

    class Meta:
        model = Listing

class MessageSerializer(serializers.ModelSerializer):
    natural_date = serializers.SerializerMethodField('get_natural_date')
    buyer_name = serializers.SerializerMethodField('get_buyer_name')
    seller_name = serializers.SerializerMethodField('get_seller_name')

    buyer = serializers.PrimaryKeyRelatedField()
    listing = serializers.PrimaryKeyRelatedField()    

    class Meta:
        model = Message
    def get_natural_date(self, obj):
        return naturaltime(obj.date)

    def get_buyer_name(self, obj):
        return obj.buyer.name

    def get_seller_name(self, obj):
        return obj.listing.user.get_profile().get_display_name()

class BuyerSerializer(serializers.ModelSerializer):
    message_set = MessageSerializer(serializers.ModelSerializer)
    class Meta:
        model = Buyer

class ListingDashboardSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    buyer_set = BuyerSerializer(required=False, many=True)
    status_lower = serializers.SerializerMethodField('get_status_lower')
    natural_date = serializers.SerializerMethodField('get_natural_date')
    class Meta:
        model = Listing

    def get_status_lower(self, obj):
        return obj.status.name.lower()

    def get_natural_date(self, obj):
        return naturaltime(obj.create_date)

class HermesSerializer(serializers.ModelSerializer):
    submarket = serializers.IntegerField(source= 'sub_market')
    manageLink = serializers.URLField(source = 'CL_link')
    cat = serializers.CharField(source = 'get_category_id')
    listingType = serializers.CharField(source = 'get_verbose_type')
    price = serializers.CharField(source = 'get_price_as_string')
    email = serializers.CharField(source = 'user.userprofile.get_rocket_email')
    photos = serializers.Field(source = 'get_photo_urls')
    poll_url = serializers.Field(source='get_poll_url')
    view_link_post_url = serializers.Field(source='get_view_link_post_url')
    phoneNumber = serializers.Field(source='user.userprofile.get_user_pn')

    class Meta:
        model = Listing
        exclude = (
            'sub_market',
            'CL_view',
            'CL_link',
            'create_date',
            'id',
            'last_modified',
            'status',
            'category',
            'listing_type',
            'user'
        )

class AdminEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = ('CL_link',)
