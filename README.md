# Rocket Listings - Django

## Setup

### Python installation

I think Python `2.7.3` is installed on OSX Mountain Lion by default, you can check this by running `python -V` in your terminal. If you don't have `2.7.3` installed for any reason, just install the homebrew version of python by running:

	brew install python 

If you don't have homebrew installed, get it installed [here](http://mxcl.github.com/homebrew/). 

Try running `python -V` again. If you don't get `2.7.3` this time, the problem likely has to do with your terminal paths. Go:

	sudo subl /etc/hosts

and edit it to look like this, before saving and closing the file:

	/usr/local/bin
	/usr/local/sbin
	/usr/bin
	/usr/sbin
	/bin
	/sbin

After restarting your terminal, the output of `python -V` should be `2.7.3`.

### Django installation

Run this:

	pip install -r requirements.txt

`pip` is one of Python's package managers. It definitely comes packaged with the homebrew version of python, but idk whether it comes with the Mountain Lion version. If you find you don't have `pip` then your should probably switch over to a homebrew python installation.

### Postgres installation

Run this to make sure that you don't have multiple versions of Postgres installed:

	brew rm --force postgres

Now download and run the [Postgres App](http://postgresapp.com/).

Name your postgres user `teddyknox` and keep the password blank. Later on I'll be changing this username to something like `rocketlistings`, but for now I want to focus on development and not postgres administration. 

### Rocket Listings installation
Run this in the folder that you want to contain the project (requires that `git` be installed):

	git clone git@github.com:Rocket-Listings/Rocket-Listings-Django.git

When that's done, cd into the new `Rocket-Listings-Django` directory and run:

	python manage.py syncdb

If that runs without errors, it means your postgres install is working. That's very very good. Think about how good that is. 

After this command, the terminal may prompt you for you to add some superuser information. This is for administration of the local site, and has nothing to do with the codebase, so feel free to put your own info in there. 

### Start the development server

Now we can start the server by running, in the same folder, this command:

	python manage.py runserver

If you direct your browser to:

	http://localhost:8000/

You'll hopefully find the new version of the Rocket Listings site.

Let's stop for a second and realize how much easier that was than setting up the PHP site with all its Rails migrations, git submodule syncing, and apache virtual hosts.