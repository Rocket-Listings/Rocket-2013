from celery import task
from celery.signals import task_success
from django.shortcuts import get_object_or_404
from listings.models import Listing

import requests
import mechanize
import cookielib

@task(name="tasks.cl_anon_autopost_task")
def cl_anon_autopost_task(data):
  #inititalize the browser
  br = mechanize.Browser()

  #set options
  br.set_handle_equiv(True)
  br.set_handle_gzip(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)

  #set debugging
  br.set_debug_http(True)
  br.set_debug_redirects(True)
  br.set_debug_responses(True)

  #set User-agent header ;)
  br.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36')]

  br.open('https://post.craigslist.org/c/brl?lang=en')
  br.select_form(nr=0)
  br.form['id'] = [data["type"]]
  br.submit()

  br.select_form(nr=0)
  br.form['id'] = [data["cat"]]
  br.submit()

  br.select_form(nr=0)
  #title
  br.form[br._pairs()[0][0]] = data["title"]
  #price
  br.form[br._pairs()[1][0]] = data["price"]
  #specific location
  br.form[br._pairs()[2][0]] = data["location"]
  #posting description  
  br.form[br._pairs()[3][0]] = data["description"]
  #email
  br.form['FromEMail'] = data["from"]
  br.form['ConfirmEMail'] = data["from"]
  r = br.submit()

  #figure out no photos case
  
  if data["photos"]:
    br.select_form(nr=0)
    for photo in data["photos"]:
      br.form.add_file(br.open_novisit(photo), filename= photo)
      br.submit()
      br.select_form(nr=0)

    br.select_form(nr=len(data["photos"])+1)
    br.submit()
  else:
    br.select_form(nr=1)
    br.submit()

  br.select_form(nr=0)
  br.submit()

  if br.geturl().endswith("mailoop"):
    payload = {'pk': data["pk"], 'success': 'True'}
    #r = requests.get(data["callback_url"], params =payload)
    #print r.text
    print "succeded"
    return payload
  else:
    payload = {'pk': data["pk"], 'success': 'False'}
    #r = requests.get(data["callback_url"], params =payload)
    print "failed"
    return payload

@task(name="tasks.cl_anon_update_task")
def cl_anon_update_task(data):
  #inititalize the browser
  br = mechanize.Browser()

  #set options
  br.set_handle_equiv(True)
  br.set_handle_gzip(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)

  #set debugging
  # br.set_debug_http(True)
  # br.set_debug_redirects(True)
  # br.set_debug_responses(True)

  #set User-agent header ;)
  br.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36')]

  br.open(data["update_url"])
  print br.geturl()

  for i, form in enumerate(br.forms()):
    if form.get_value(name = "go") == "Cancel Edit":
      print "FOUND"
      br.select_form(nr = i)
      br.submit()

  br.select_form(nr = 0)
  r = br.submit()
  print r.read()

  for form in br.forms():
    print form

  br.select_form(nr=0)

  if data["title"]:
    br.form[br._pairs()[0][0]] = data["title"]

  if data["price"]:
    br.form[br._pairs()[1][0]] = data["price"]

  if data["location"]:
    br.form[br._pairs()[2][0]] = data["location"]

  if data["description"]:
    br.form[br._pairs()[3][0]] = data["description"]

  if data["cat"]:
    br.form["CategoryID"] = [data["cat"]]

  print br.submit().read()

  if len(list(br.forms())) != 3:
    while len(list(br.forms())) > 3:
      print br.geturl()
      br.select_form(nr=1)
      br.submit()
      print br.geturl()

  for form in br.forms():
    print form

  if data["photos"]:
    br.select_form(nr=0)
    for photo in data["photos"]:
      br.form.add_file(br.open_novisit(photo), filename= photo)
      br.submit()
      br.select_form(nr=0)

    br.select_form(nr=len(data["photos"])+1)
    print br.submit().read()
  else:
    br.select_form(nr=len(data["photos"])+1)
    br.submit()


  br.select_form(nr=0)
  r = br.submit()
  print r.read()
  if br.geturl().endswith("redirect"):
    payload = {'pk': data["pk"], 'success': 'True'}
    return payload
    #r = requests.get(data["callback_url"], params =payload)
    #print r.text
    print "succeded"

  else:
    payload = {'pk': data["pk"], 'success': 'False'}
    return payload
    #r = requests.get(data["callback_url"], params =payload)
    print "failed"

@task(name="tasks.cl_delete_task")
def cl_delete_task(data):
  #inititalize the browser
  br = mechanize.Browser()

  #set options
  br.set_handle_equiv(True)
  br.set_handle_gzip(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)

  #set debugging
  br.set_debug_http(True)
  br.set_debug_redirects(True)
  br.set_debug_responses(True)

  #set User-agent header ;)
  br.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36')]

  br.open(data["update_url"])

  for i, form in enumerate(br.forms()):
    if form.get_value(name = "go") == "Cancel Edit":
      print "FOUND"
      br.select_form(nr = i)
      br.submit()

  br.select_form(nr=1)
  br.submit()
  br.select_form(nr=1)
  br.submit()

  return data['pk']

@task_success.connect
def celery_task_success_handler(sender=None, result=None, args=None, kwargs=None, **kwds):
  if sender.name == "tasks.cl_anon_autopost_task":
    if result['success'] == 'True':
      listing = get_object_or_404(Listing, pk=result['pk'])
      listing.status_id = 3
      listing.save()
    else:
      print "Tried to autopost listing " + str(result['pk']) + ". Failed."
  elif sender.name == "tasks.cl_anon_update_task":
    if result['success'] == 'True':
      print "Successfully autoposted listing " + str(result['pk'])
    else:
      print "Tried to update listing " + str(result['pk']) + ". Failed."
  elif sender.name == "tasks.cl_delete_task":
    print "Successfully deleted listing " + str(result)
