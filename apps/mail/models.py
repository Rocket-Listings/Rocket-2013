from django.db import models

class mailgun(models.Model):
	recipient = models.CharField(max_length=255, blank=True)
	sender = models.CharField(max_length=255, blank=True)
	frm = models.CharField(max_length=255, blank=True) #instead of from b/c from is a python reserved word
	subject = models.CharField(max_length=255, blank=True)
	body = models.TextField()
	text = models.TextField(null = True)
	signature = models.TextField(blank=True, null = True)
	timestamp = models.IntegerField(null = True)
	token = models.CharField(max_length=50, blank=True)
	sig = models.CharField(max_length=255, blank=True)
	
