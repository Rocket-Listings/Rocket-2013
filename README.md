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

## Development Stuff

### Conventions

#### CSS

We're using only classes (rather than ids). I used to think this was stupid, but now I've realized that not having to worry about whether any given selector is a class or an id is actually really nice. Also it encourages generic styling, i.e. reusing style on different stuff.

We're also using all lowercase class names, with multiple rules separate by hyphens ('-'). The naming convention is pretty arbitrary, but I want to keep it consistent. While I like camelCase a lot, I think it's less flexible and harder to read sometimes. But again, we're only doing this for consistency, not because one convention is better than another.

We've switched over to doing our styles using LESS styling. Less is a "dynamic stylesheet language" which affords us a lot more power and a lot less redundant when styling. Read up on it at [LessCss.org](http://lesscss.org/). With it, we can nest our styling rules, so that there's MUCH less repetition. After you get used to it (A) you'll find that CSS is much easier to read. (B) you'll have a hard time going back to plain CSS. Also things like mixins and variables are awesome also. Less stylesheets are not valid CSS obviously, so they need to be compiled to CSS before being served up to the web browser. Usually you'd have to do the conversion using a command-line every time you make a change to the .less file, but using this nifty [OSX app aptly called Less.app](http://incident57.com/less/) you can add folder which you want the app to watch. After you do this, the app will automatically recompile the less files whenever you save new changes, placing .css files with the same name in the same directory. I usually keep this app open in the background as I code. __With all this in mind, never directly edit the .css files, or your changes will be overwritten the next time the .less files are compiled__. 

The LESS+CSS files are separated by "application". (An application in Django is any modular part of a project. So our project here is Rocket Listings, and our applications right now include 'listings', 'accounts', 'static_pages', and will later on include 'payment', 'api' and other separate stuff. Applications are separated by folder; those folders are in the project root (inside `Rocket-Listings-Django`).) Within each application's folder, you'll find another folder called `static` that holds all the static resources for that application. Static resources are resources that aren't dynamic. Templates are dynamic, because they're not served up to the user 'as-is', but instead have all kinds of custom data plugged into them. But css files, images, and javascript files are static, because they remain the same no matter what. So within this `static` folder you'll find a bunch of other folders with the relevant js, css, less, and images for a given application. The 'rocketlistings' application is special because it represents the header and footer templates and static resources for the whole site. Global styles for things that appear on every page of the site go in the global.less stylesheet in the 'rocketlistings' app. Static pages (pages that themselves don't change much at all) like the homepage and FAQ page are all kept in the 'static\_pages' app.

So separating static resources by application is really helpful from an organizational standpoint, but not from technical standpoint. When we eventually deploy to production, want to be able to serve these static files using a real server, not just the Django development server. 'Real' servers include 'Apache', 'Lighttpd', 'nginx' and a few other. These servers excel at returning static files over http. So we want to let the real server do the work of returning the static files. We also want our static resources to have nice urls like this:

	http://www.rocketlistings.com/static/img/logo.png
	http://www.rocketlistings.com/static/css/global.css
	http://www.rocketlistings.com/static/js/ajaxupload.js

We want the URLs to look like that no matter what application the resources are coming from. The problem is that the way the 'real' servers are set up, we'd have to point them to the 'static' folder of each app separately, instead of having one big combinded folder of static files. Django anticipates this problem, and auto-fills a folder in the project root called 'staic_collected' which contains all of these static files (but still organized in their respective 'css', 'js', or 'img' folders). This makes it much easier to serve up these files later on. Ignore the 'static_collected' folder when you're developing -- it should be kept empty. Whenever you go

	python manage.py runserver

That folder will be populated with all the static content.


