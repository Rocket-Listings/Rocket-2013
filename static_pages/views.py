from django.shortcuts import render_to_response

def help(request):
	return render_to_response('help.html')

def contact(request):
	return render_to_response('contact.html')

def faq(request):
	return render_to_response('faq.html')

def about(request):
	return render_to_response('about.html')