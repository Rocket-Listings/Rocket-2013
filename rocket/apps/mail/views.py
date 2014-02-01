from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from celery import chain, chord
from listings.models import Buyer, Message, Listing
from listings.forms import MessageForm
from mail.tasks import send_message_task, new_cl_admin_message_task, lookup_view_links_task, process_new_cl_message_task



import re
import hashlib, hmac

def verify(token, timestamp, signature):
	"""this function secures the webhook by:
	Concatenating timestamp and token values.
	Encoding the resulting string with the HMAC algorithm (using your API Key as a key and SHA256 digest mode).
	Comparing the resulting hexdigest to the signature."""

	api_key = settings.MAILGUN_ACCESS_KEY
	return signature == hmac.new(
                             key=api_key,
                             msg='{}{}'.format(timestamp, token),
                             digestmod=hashlib.sha256).hexdigest()

@csrf_exempt
@require_POST
def on_incoming_test_message(request):
	timestamp = request.POST.get('timestamp', '')
	token = request.POST.get('token', '')
	sig = request.POST.get('signature', '')
	if verify(token, timestamp, sig):
		print "Received unrouted Rocket Dev message."
		# mime = request.POST.get('message-headers')
		# print mime
		# sender = request.POST.get('sender')
		# print sender
		# recipient = request.POST.get('recipient')
		# print recipient
		# subject   = request.POST.get('subject', '')
		# print subject
		# frm = request.POST.get('from', '')
		# print frm
		body = request.POST.get('body-plain', '')
		print body
		# body_html = request.POST.get('body-html', '')
		# print body_html
		# text = request.POST.get('stripped-text', '')
		# print text
		# signature = request.POST.get('stripped-signature', '')
		# print signature
		return HttpResponse('OK')
	else:
		return HttpResponse('Unauthorized')

@csrf_exempt
@require_POST
def new_cl_admin_message(request):
	if verify(request.POST.get('token', ''), request.POST.get('timestamp', ''), request.POST.get('signature', '')):
		_listing_title = request.POST.get('subject', '').partition('"')[2].partition('"')[0]
		_listing_title = re.sub(r'(?<=/) ', '', _listing_title)
		listing_title = _listing_title.lstrip()
		msg_dict = {
			'username': request.POST.get('recipient').split('@')[0],
			'listing_title': listing_title,
			'body': request.POST.get('body-html', '')
		}
		new_cl_admin_message_task.delay(msg_dict)
		return HttpResponse('OK')
	return HttpResponse('Unauthorized')

@csrf_exempt
@require_POST
def new_cl_buyer_message(request):
	if verify(request.POST.get('token', ''), request.POST.get('timestamp', ''), request.POST.get('signature', '')):
		user = get_object_or_404(User, username=request.POST.get('recipient').split('@')[0])
		buyer_name = request.POST.get('from', '').partition("\"")[2].partition("\"")[0]
		buyer_email = request.POST.get('from', '').partition("<")[2].partition(">")[0]
		msg_parts = request.POST.get('body-plain', '').split('------------------------------------------------------------------------')
		msg_body = request.POST.get('stripped-text', '')
		listing_view_link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg_parts[1])[0]
		message_dict = {'listing_view_link': listing_view_link,
										'buyer_name': buyer_name,
										'buyer_email': buyer_email}
		try:
			listing = user.listing_set.get(CL_view=listing_view_link)
			message = Message(listing=listing, content=msg_body, isSeller=False)
			message.save()
			message_dict['message_id'] = message.id
			process_new_cl_message_task.delay(**message_dict)
		except Listing.DoesNotExist:
			listings_no_links = map(lambda l: l.id, user.listing_set.filter(Q(CL_view="") | Q(CL_view=None)))
			message = Message(content=msg_body, isSeller=False)
			message.save()
			message_dict['message_id'] = message.id
			print listings_no_links
			lookup_view_links_task.apply_async((listings_no_links), link=process_new_cl_message_task.s(**message_dict))
			#chord(lookup_view_links_task.map(listings_no_links) | process_new_cl_message_task(**message_dict))()
		return HttpResponse('OK')
	else:
		return HttpResponse('Unauthorized')

@csrf_exempt
@require_POST
def new_rocket_message(request, is_seller, thread):
	if verify(request.POST.get("token", ""), request.POST.get("timestamp", ""), request.POST.get("signature", "")):
		buyer_hash = thread
		SHA1_RE = re.compile('^[a-f0-9]{40}$')
		if SHA1_RE.search(buyer_hash):
			buyer = Buyer.objects.get(rocket_address=buyer_hash)
			message_dict = { 
				'listing': buyer.listing.id,
				'buyer': buyer.id,
				'content': request.POST.get('stripped-text'),
				'isSeller': is_seller == 'True'
			}
			message_form = MessageForm(message_dict)
			if message_form.is_valid():
				message = message_form.save()
				send_message_task.delay(message.id)
				return HttpResponse("OK")
	return HttpResponse("Unauthorized")
