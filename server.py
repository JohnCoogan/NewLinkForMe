'''
NewLinkFor.me
'''
import flask, twitter, tweepy, json, pymongo

app = flask.Flask(__name__)

# Config
CONSUMER_TOKEN='enter token here'
CONSUMER_SECRET='enter secret here'
CALLBACK_URL = 'enter callback url here'
MONGOLAB_URI = 'mongodb://username:password@ds037617-a.mongolab.com:37617/database'
db = pymongo.Connection(MONGOLAB_URI)
users = db.database.users # Set this to the name of your database.
session = dict()

# Home route, generates a link to start OAuth flow.
@app.route("/")
def send_token():
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET, CALLBACK_URL)
	
	try: 
		# Get the request tokens
		redirect_url = auth.get_authorization_url()
		session['request_token'] = (auth.request_token.key, auth.request_token.secret)
	except tweepy.TweepError:
		print 'Error! Failed to get request token'
	
	# This is twitter's url for authentication
	return flask.render_template('home.html', authurl=redirect_url)

# Callback handler. 
@app.route("/verify")
def get_verification():
	
	#get the verifier key from the request url
	verifier= flask.request.args['oauth_verifier']
	
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	token = session['request_token']
	del session['request_token']
	
	auth.set_request_token(token[0], token[1])

	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		print 'Error! Failed to get access token.'
	
	# now you have access!
	api = tweepy.API(auth)

	# Store in the database.
	username = api.verify_credentials().screen_name
	user = users.find_one({"screen_name": username})
	if user is None:
		newuser = {"screen_name": username,
			"access_token_key": auth.access_token.key,
			"access_token_secret": auth.access_token.secret,
			"full_feed": "[]",
			"read_feed": "[]"}
		users.insert(newuser)
	return flask.redirect('/user/' + username)
	
# Give the user their personalized link.
@app.route("/user/<username>")
def user(username):
	return flask.render_template('user.html', userlink = '/link/' + username)	

# Gets the next unread link for a particular user.
@app.route('/link/<username>')
def show_user_profile(username):
	# Loads the user's data from the database.
	user = users.find_one({"screen_name": username})
	# pulls both feeds for the user and compares them.
	full_feed = json.loads(user['full_feed'])
	read_feed = json.loads(user['read_feed'])
	# If the user doesn't have links yet, go and get some.
	if not full_feed:
		full_feed = update_full_feed(username)
	# Create an list of unread links by comparing the full_feed to the read_feed.
	unread_feed = list(set(full_feed).difference(set(read_feed)))
	# If there is an unread link, serve it to the user and add it to the read list. 
	if unread_feed:
		redirectlink = unread_feed.pop(0)
		read_feed.append(redirectlink)
		users.update({"screen_name": username}, {"$set": {"read_feed": json.dumps(read_feed)}})
		return flask.redirect(redirectlink)
	# If there are no more links, check for more.
	else:
		update_full_feed(username)
		return flask.render_template('error.html', userlink = '/link/' + username)

# Get 200 tweets and saves the links.
def get_feed_links(username):
	# Get Twitter API Keys from User Object
	user = users.find_one({"screen_name": username})
	feed = []
	api = twitter.Twitter(auth=twitter.OAuth(user['access_token_key'], user['access_token_secret'], CONSUMER_TOKEN, CONSUMER_SECRET))
	# Iterate over status objects and see if they have urls.
	for status in api.statuses.home_timeline(count=200, include_entities="true"):
		if status['entities']['urls']:
			feed.append(status['entities']['urls'][0]['expanded_url'])
	return feed

# Gets the most recent links and adds new links to the full feed list.
def update_full_feed(username):
	user = users.find_one({"screen_name": username})
	full_feed = json.loads(user['full_feed'])
	my_feed = get_feed_links(username)
	new_media_list = list(set(my_feed).difference(set(full_feed)))
	updated_full_feed = full_feed + new_media_list
	users.update({"screen_name": username}, {"$set": {"full_feed": json.dumps(updated_full_feed)}})
	return updated_full_feed

# Runs the app with debug on. Change for production.
if __name__ == "__main__":
	app.run(debug=True)