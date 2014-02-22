# Rocket Listings - Django

_Last updated: 2/22/14_

Read the Rocket [Wiki](https://github.com/Rocket-Listings/Rocket/wiki) to find all the notes that used to be in this huge file.

This file will now serve as a message board for Rocket devs.
---
Restart the new relic agent with:

    heroku run newrelic-admin validate-config --app rocket-listings - stdout

Removing new relic prefix to see if it solves db issue.

Was: `web: newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi`
Now: `gunicorn -c gunicorn.py.ini wsgi`