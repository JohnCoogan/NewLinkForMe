<<<<<<< HEAD
New Link For Me
============

What is this?
-------------

A simple Flask [Flask](http://flask.pocoo.org/) app running on
[Heroku](https://www.heroku.com/) that lets you stumble upon random links from your twitter feed.

The app demonstrates a complete OAuth flow through the [Twitter API](http://dev.twitter.com) and subsequently stores user keys in a [MongoLab](http://www.mongolab.com) instance using the [PyMongo](http://pypi.python.org/pypi/pymongo) driver. Upon authenticating the user, [Python Twitter Tools](http://mike.verdone.ca/twitter) is used to pull the most recent 200 tweets from a user's feed and then save links out of any tweets that contain them. All of this logic can be seen in the server.py file that drives the entire app.

Additionally, the app uses [Twitter's Bootstrap
project](http://twitter.github.com/bootstrap/), [Less
CSS](http://lesscss.org/), and, in Heroku's production environment, is served through [`gunicorn`](http://gunicorn.org/).


Instructions
------------

First, you'll need to clone the repo.

    $ git clone git@github.com:johncoogan/newlinkforme.git
    $ cd newlinkforme

Second, let's download `pip`, `virtualenv`, `foreman`, and the [`heroku`
Ruby gem](http://devcenter.heroku.com/articles/using-the-cli).

    $ sudo easy_install pip
    $ sudo pip install virtualenv
    $ sudo gem install foreman heroku

Now, you can setup an isolated environment with `virtualenv`.

    $ virtualenv venv --distribute
    $ source venv/bin/activate


Installing Packages
--------------------

### Gunicorn

To use `gunicorn`, you just need to set the `Procfile` and `requirements.txt`.

First, check that the `Procfile` looks like the following:

    web: gunicorn server:app -b 0.0.0.0:$PORT

This follows the standard [Heroku Python deployment steps](https://devcenter.heroku.com/articles/python).

### pip

Then, let's get the requirements installed in your isolated test
environment.

    $ pip install -r requirements.txt


Twitter Keys
------------------------

If you haven't already, get signup for a [Twitter Developer Account.](https://dev.twitter.com/user/login)

After you have signed up, you will need to [create a new application.](https://dev.twitter.com/apps/new)

For testing, set the call back URL to http://localhost:5000/verify

Copy your consumer token and consumer secret over to the configuration section of the server.py file. 

These keys identify your app to Twitter's API and allow you to verify requests.


MongoLab Database
------------------------
MongoLab is a cloud-based database provider that hosts MongoDB databases and is closely integrated with Heroku. [Create an account](https://mongolab.com) and create a new database. 

Once you have created your database, you can easily add the URI to the server.py file to allow the PyMongo package to connect and create records as needed.

Your URL will look like this:
	mongodb://<user>:<password>@ds037617-a.mongolab.com:37617/database


Running Your Application
------------------------

Now, you can run the application locally.

    $ foreman start

This will run the app method within the server.py (as described in the Procfile) and server the app on http://localhost:5000.


Deploying
---------

If you haven't [signed up for Heroku](https://api.heroku.com/signup), go
ahead and do that. You should then be able to [add your SSH key to
Heroku](http://devcenter.heroku.com/articles/quickstart), and also
`heroku login` from the commandline.

Now, to upload your application, you'll first need to do the
following -- and obviously change `app_name` to the name of your
application:

    $ heroku create app_name -s cedar

And, then you can push your application up to Heroku.

    $ git push heroku master

Finally, we can make sure the application is up and running.

    $ heroku ps

Now, we can view the application in our web browser.

    $ heroku open

And, to deactivate `virtualenv` (once you've finished coding), you
simply run the following command:

    $ deactivate


Next Steps
----------

After you've got your application up and running, there a couple next
steps you should consider following.

1. Create a new `README.md` file.
2. Add your Google Analytics ID to the `base.html` template.
3. Adjust the `author` and `description` `<meta>` tags in the
   `base.html` template.
4. Change the `robots.txt` and `favicon.ico` files in the `static`
   directory.
5. Change the `apple-touch` icons in the `static` directory.


Reactivating the Virtual Environment
------------------------------------

If you haven't worked with `virtualenv` before, you'll need to
reactivate the environment everytime you close or reload your terminal.

    $ source env/bin/activate

If you don't reactivate the environment, then you'll probably receive a
screen full of errors when trying to run the application locally.


Adding Requirements
-------------------

In the course of creating your application, you may find yourself
installing various Python modules with `pip` -- in which case you'll
need to update the `requirements.txt` file. One way that this can be
done is with `pip freeze`.

    $ pip freeze > requirements.txt


Custom Domains
--------------

If your account is verified -- and your credit card is on file -- you
can also easily add a custom domain to your application.

    $ heroku addons:add custom_domains
    $ heroku domains:add www.mydomainname.com

You can add a [naked domain
name](http://devcenter.heroku.com/articles/custom-domains), too.

    $ heroku domains:add mydomainname.com

Lastly, add the following A records to your DNS management tool.

    75.101.163.44
    75.101.145.87
    174.129.212.2
=======
NewLinkForMe
============

Stumble Upon for Your Twitter Feed
>>>>>>> 774d3379b5a0e1cc22b4fe72edf6829c4f414d37
