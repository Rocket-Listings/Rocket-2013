from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from users.decorators import first_visit, view_count
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from operator import __add__

from listings.models import Listing, Message, Spec, ListingPhoto
from listings.serializers import ListingSerializer, SpecSerializer, ListingPhotoSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from haystack.query import SearchQuerySet

# Listing API
class ListingList(APIView):
    """
    List all listings, or create a new listing.
    """
    def pre_save(self, obj):
        obj.user = self.request.user

    def get(self, request, format=None):
        listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ListingSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ListingDetail(APIView):
    """
    Retrieve, update or delete a listing instance.
    """
    # def pre_save(self, obj):
    #     obj.user = self.request.user

    def get_object(self, pk):
        try:
            return Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        listing = self.get_object(pk)
        serializer = ListingSerializer(listing, partial=True, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        listing = self.get_object(pk)
        listing.delete()
        return Response(status=204)

class SpecList(APIView):
    """
    List all specs, or create a new spec.
    """
    def pre_save(self, obj):
        obj.user = self.request.user

    def get(self, request, format=None):
        specs = Spec.objects.all()
        serializer = SpecSerializer(specs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SpecSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class SpecDetail(APIView):
    """
    Retrieve, update or delete a spec instance.
    """
    # def pre_save(self, obj):
    #     obj.user = self.request.user

    def get_object(self, pk):
        try:
            return Spec.objects.get(pk=pk)
        except Spec.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        spec = self.get_object(pk)
        serializer = SpecSerializer(spec)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        spec = self.get_object(pk)
        serializer = SpecSerializer(spec, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        spec = self.get_object(pk)
        serializer = SpecSerializer(spec, partial=True, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        spec = self.get_object(pk)
        spec.delete()
        return Response(status=204)

class ListingPhotoList(APIView):
    """
    List all photos, or create a new photo.
    """
    def pre_save(self, obj):
        obj.user = self.request.user

    def get(self, request, format=None):
        photos = ListingPhoto.objects.all()
        serializer = ListingPhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ListingPhotoSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ListingPhotoDetail(APIView):
    """
    Retrieve, update or delete a photo instance.
    """
    # def pre_save(self, obj):
    #     obj.user = self.request.user

    def get_object(self, pk):
        try:
            return ListingPhoto.objects.get(pk=pk)
        except ListingPhoto.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = ListingPhotoSerializer(photo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = ListingPhotoSerializer(photo, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = ListingPhotoSerializer(photo, partial=True, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        photo = self.get_object(pk)
        photo.delete()
        return Response(status=204)

def delete(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user == listing.user:
        # remove listing from haystack index
        haystack.connections['default'].get_unified_index().get_index(Listing).remove_object(listing)
        cl_cxt = {'update_url': listing.CL_link, 'pk': listing.pk}
        if not settings.AUTOPOST_DEBUG:
            cl_delete_task.delay(cl_cxt)
        listing.delete()
        return HttpResponse(200)
    else:
        return HttpResponse(403)

def search_ajax(request):
    search_text = request.REQUEST.get('search', '').strip()
    listings = SearchQuerySet().filter(content=search_text)[:20]
    cxt = { 'listings': listings }
    # for listing in listings:
        # listing.url_id = reverse('listings.views.detail', args=[str(listing.url_id)])
    return TemplateResponse(request, 'listings/partials/ajax_search.html', cxt)

@require_GET
def status(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return HttpResponse(listing.status)

@require_GET
def update_status(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user == listing.user:
        new_status = request.GET.get('status', '')
        status_dict = {'Draft': 1, 'Pending': 2, 'Active': 3, 'Sold': 4, 'Deleted': 5}
        if new_status in status_dict:
            listing.status_id = status_dict[new_status]
            listing.save()
            response_dict = {'id': listing.id, 'status': listing.status.name}
            return HttpResponse(simplejson.dumps({'listing': response_dict, 'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'listing': listing.id, 'status': 'status error'}), content_type='application/json')
    else:
        return HttpResponse(403)


@require_GET
def dashboard_data(request):
    user = request.user
    ids = map(lambda i: int(request.GET.get(i, '0')), ['listing', 'buyer', 'message'])

    listings = Listing.objects.filter(user=user).order_by('-create_date').all()
    buyers = reduce(__add__, map(lambda l: list(l.buyer_set.all()), listings), [])
    messages = reduce(__add__, map(lambda b: list(b.message_set.all()), buyers), [])
    latest_ids = map(lambda set: map(lambda i: i.id, set), [listings, buyers, messages])
    for i, val in enumerate(latest_ids):
        try:
            latest_ids[i] = max(val)
        except ValueError:
            latest_ids[i] = 0

    listings_data = map(lambda l: {
        'title': l.title, 
        'link': l.get_absolute_url(), 
        'id': l.id, 
        'price': l.price, 
        'category': l.category.name, 
        'status': l.status.name,
        'status_lower': l.status.name.lower(),
        'sort_date': l.create_date.strftime("%m/%d/%y %I:%M %p"),
        'natural_date': naturaltime(l.create_date)}, listings.filter(id__gt=ids[0]))
    buyers_data = map(lambda b: {
        'listing_id': b.listing.id, 
        'buyer_id': b.id, 
        'max_offer': b.curMaxOffer, 
        'name': b.name, 
        'last_message_date': naturaltime(b.last_message().date)}, [b for b in reversed(buyers) if b.id > ids[1]])
    messages_data = map(lambda m: {
        'isSeller': m.isSeller,
        'buyer_id': m.buyer.id,
        'buyer_name': m.buyer.name,
        'seller_name': m.listing.user.get_profile().get_display_name(),
        'listing_id': m.listing.id,
        'message_id': m.id,
        'content': m.content,
        'date': naturaltime(m.date)}, [m for m in messages if m.id > ids[2]])

    json = {'listings': listings_data, 'buyers': buyers_data, 'messages': messages_data, 'latest': latest_ids}
    return HttpResponse(simplejson.dumps(json), content_type="application/json")

@require_POST
def dashboard_message(request):
    if request.POST.get("content", ""):
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.isSeller = True
            message.save()
            send_message_task.delay(message.id)
            response_data = { 'listing_id': message.listing.id,
                              'isSeller': message.isSeller,
                              'seller_name': message.listing.user.get_profile().get_display_name(),
                              'buyer_id': message.buyer.id,
                              'buyer_name': message.buyer.name,
                              'content': message.content,
                              'message_id': message.id,
                              'date': naturaltime(message.date) }
            return HttpResponse(simplejson.dumps({'messages': response_data, 'status': 'success'}), content_type="application/json")
        else:
            return HttpResponse(simplejson.dumps({'errors': message_form.errors, 'status': 'err_validation'}), content_type="application/json")
    else:
        return HttpResponse(simplejson.dumps({'errors': 'Message content is empty.', 'status': 'err_empty'}))

@require_GET
@login_required
def message_seen(request):
    message = get_object_or_404(Message, id=request.GET.get("message_id", ""))
    if request.user == message.listing.user:
        message.seen = True
        message.save()
        msg_dict = {'message_id': message.id,
                    'buyer_id': message.buyer.id,
                    'listing_id': message.listing.id,
                    'listing_all_read': all(map(lambda m: m.seen, message.listing.message_set.all()))}
        return HttpResponse(simplejson.dumps({'message_data': msg_dict, 'status': 'success'}), content_type="application/json")
    else:
        return HttpResponse(simplejson.dumps({'status': 'Error: This action is forbidden.'}), content_type="application/json")
