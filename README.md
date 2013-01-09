# Rocket Listings - Django

## Setup

### Python installation

I think Python `2.7.3` is installed on OSX Mountain Lion by default, you can check this by running `python -V` in your terminal. If you don't have `2.7.3` installed for any reason, just install the homebrew version of python by running:

	brew install python 

If you don't have homebrew installed, get it installed [here](http://mxcl.github.com/homebrew/). 

Try running `python -V` again. If you don't get `2.7.3` this time, the problem likely has to do with your terminal paths. Go:

	nano ~/.bash_profile

and add the following line to the top:

	export PATH=/usr/local/bin:$PATH

After restarting your terminal tab, the output of `python -V` should be `2.7.3`.

### Django installation


Let's see if `pip`, a python package manager is installed on the system by running:

	which pip

If that spits out a file path, you're good to go, otherwise, run `sudo easy_install pip` and you'll be good.

This next line installs all of our project's dependencies.

	pip install -r requirements.txt


### Postgres installation

First remove any broken postgres installations you may have.

Now we install Postgres:

	brew install postgres

Homebrew will print out some instructions on registering the DB with OSX to start up on boot, but if you mind having Postgres running all the time, you can just start postgres on an as-needed basis in a new terminal tab by running the command homebrew gives you.

If you want to see all the info about the `postgres` installation again later, you can go `brew info postgres`.

Your postgres database name is `postgres` by default. Your postgres username is your `OS` username by default, and the default password is blank.

### Rocket Listings installation

Run this in the folder that you want to contain the project (requires `git`):

	git clone git@github.com:Rocket-Listings/Rocket-Listings-Django.git

Open up Sublime text and in the top menu go `Project -> Add Folder to Project`, and select `Rocket-Listings-Django`. After this we save the project by going `Project -> Save project as..` and saving the project file inside `Rocket-Listings-Django`, naming it whatever you want. From now on, to open the project, you can open Sublime Text, and hit Command+Control+P to open a dialog to select a project. Clicking on the project you want to open will open it. Having Sublime Text Projects allow you to have all kinds of cool stuff the file browser sidebar among other things.

In sublime text, open `Rocket-Listings-Django/rocketlistings/settings_dev_template.py`, and enter your Postgres username where indicated. Save the file not as `settings_dev_template.py`, but as `settings_dev.py`. You can do a `save_as` by going Command+Shift+S.

Going back to the terminal, inside the project root directory (`Rocket-Listings-Django`) run this:

	python manage.py syncdb

This adds all the DB tables you need for the project to work.

If that runs without errors, it means your postgres install is working. That's very very good. Think about how good that is. 

After this command, the terminal may prompt you for you to add some superuser information. This is for administration of the local site, and has nothing to do with the codebase, so feel free to put your own info in there. 

### Start the development server

Now we can start the server by running, in the same teminal location, this command:

	python manage.py runserver

If you direct your browser to:

	http://localhost:8000/

You'll hopefully find the new version of the Rocket Listings site.

Let's stop for a second and realize how much easier that was than setting up the PHP site with all its Rails migrations, git submodule syncing, and apache virtual hosts.

## Development Stuff

### Tricks (?!)

#### Shorten `python manage.py`
If you're tired of typing `python manange.py runserver`,

you can make `manage.py` executable by running:
	
	chmod 755 manage.py

And now you can instead type:
	
	./manage.py runserver

Sort of faster...


#### Reduce clutter in sublime project sidebar files

If you haven't already, go ahead and create a sublime text project around the root project folder. Save the project as whatever and place the project file inside that root project folder. Our `.gitignore` file knows to ignore those types of files. This makes it so that you can have this nifty sidebar which shows you all of the project files. Right now, all of our project files show up: `.py`, `.html`, the `.png`, and even the `__init__.py` files. But we kinda don't want that, since you're never going to want to edit an image in the text editor, and you want to ignore `__init__.py` files. To make Sublime text ignore these types of files, open up your `.sublime-project` file (you may have to go `File -> Open...` to see it). and make it look like this (with the exception of the `path` field):

	{
		"folders":
		[
			{
				"path": "<KEEP THIS FIELD THE SAME>",
				"file_exclude_patterns":[
					"*.sublime-project",
					"*.sublime-workspace",
					"*.css",
					"__init__.py",
					".gitignore"
				],
	        	"folder_exclude_patterns": [
	           		"img",
	           		"static_collected"
	        	]
			}
		]
	}

You should have much less visual clutter when looking through your project folders now.

### Conventions

#### CSS

We're using only classes (rather than ids). I used to think this was stupid, but now I've realized that not having to worry about whether any given selector is a class or an id is actually really nice. Also it encourages generic styling, i.e. reusing style on different stuff.

We're also using all lowercase class names, with multiple words separate by hyphens ('-'). The naming convention is pretty arbitrary, but I want to keep it consistent. While I like camelCase a lot, I think it's less flexible and harder to read sometimes. But again, we're only doing this for consistency, not because one convention is much better than another.

We've switched over to doing our styles using LESS styling. Less is a "dynamic stylesheet language" which affords us a lot more power and a lot less redundancy when styling. Read up on it at [LessCss.org](http://lesscss.org/). With it, we can nest our styling rules, so that there's MUCH less repetition. After you get used to it doing styles becomes a lot less painful and disorganized. Features like mixins and variables are also great. Less stylesheets are not valid CSS obviously, so they need to be compiled to CSS before being served up to the web browser. Usually you'd have to do the conversion using a command-line program every time you'd make a change to a .less file, but using this nifty [OSX app called Less.app](http://incident57.com/less/) you can specify folders containing .less files that you want to be automatically compiled to .css files. So the app will automatically recompile the less files whenever you save changes, placing .css files with the same names in the same directory. I set the app up with all of the project's `static/css` folders, and usually keep this app open in the background when I work. __With all this in mind, never directly edit the .css files, or your changes will probably be overwritten the next time the corresponding .less files are compiled__. 

The .less and .css files are separated by "application". An application in Django is any modular part of a project. So our project here is Rocket Listings, and our applications right now include 'listings', 'accounts', 'static_pages', and will later on include 'payment', 'api' and other separate stuff. Applications are separated by folder; those folders are in the project root (inside `Rocket-Listings-Django`). Within each application's folder, you'll find another folder called `static` that holds all the static resources for that application. Static resources are resources that aren't dynamic. Templates are dynamic, because they're not served up to the user 'as-is', but instead have all kinds of custom data plugged into them. But css files, images, and javascript files are static, because they remain the same no matter what. So within this `static` folder you'll find a bunch of other folders with the relevant js, css, less, and images for a given application. The 'rocketlistings' application is special because it represents the header and footer templates and static resources for the whole site. Global styles for things that appear on every page of the site go in the global.less stylesheet in the 'rocketlistings' app. Static pages (pages that themselves don't change much at all) like the homepage and FAQ page are all kept in the 'static\_pages' app.

So separating static resources by application is really helpful from an organizational standpoint, but not from technical standpoint. When we eventually deploy to production, want to be able to serve these static files using a real server, not just the Django development server. 'Real' servers include 'Apache', 'Lighttpd', 'nginx' and a few other. These servers excel at returning static files over http. So we want to let the real server do the work of returning the static files. We also want our static resources to have nice urls like this:

	http://www.rocketlistings.com/static/img/logo.png
	http://www.rocketlistings.com/static/css/global.css
	http://www.rocketlistings.com/static/js/ajaxupload.js

We want the URLs to look like that no matter what application the resources are coming from. The problem is that the way the 'real' servers are set up, we'd have to point them to the 'static' folder of each app separately, instead of having one big combinded folder of static files. Django anticipates this problem, and, when getting ready to deploy, populates a folder in the project root called `staic_collected` to contain all of these static files (but still organized in their respective 'css', 'js', or 'img' folders). This makes it much easier to serve up these files later on. Since we're not getting ready to deploy anytime soon, `static_collected` is kept empty, and you can ignore that folder when you're developing. Actually, since that folder isn't even in version control, you really have nothing to worry about at all. 