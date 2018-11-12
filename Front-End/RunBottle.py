import bottle
import httplib2
import json
import redis
from collections import defaultdict
from apiclient.discovery import build
from googleapiclient.errors import HttpError
from beaker.middleware import SessionMiddleware
from bottle import route, run, get, post, request, static_file, template, error
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow

# Constants
HOME = "http://localhost:8080/"
CLIENT_SECRET = "woMB_Z4XCZTyAW_-2hdUNpfx"
REDIRECT = "http://localhost:8080/redirect"
SCOPE = "https://www.googleapis.com/auth/userinfo.email"
CLIENT_ID = "547443438769-9q9tatcnkpv6g05cj9d9ds98n0q661t1.apps.googleusercontent.com"

# Beaker session options
session_opts={
    'session.type':'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto' : True
}

app_middleware = SessionMiddleware(bottle.app(), session_opts)

# Global dictionary used to store history tables for every user
searchHistory = {}

# Retrieve beaker session before every route
@bottle.hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

# Route used to service .css file requests
@route('<filename:re:.*\.css>', name="static")
def css(filename):
    print ("css:" + filename)
    return static_file(filename, root='./styles')

# Route used to service .js file requests
@route('<filename:re:.*\.js>', name="static")
def js(filename):
    print ("js:" + filename)
    return static_file(filename, root='./scripts')

# Route used to service .jpg file requests
@route('<filename:re:.*\.png>', name="static")
def png(filename):
    print ("png:" + filename)
    return static_file(filename, root='./images')

@route('./error')
@error(404)
def error404(error):
    return template('./views/error.html', root='./')

# Display main search engine page without showing any tables by default
@route('/')
def hello():
    # Check if user is logged in
    if "logged_in" in request.session and request.session["logged_in"] is True:
        userID = request.session["id"]
        userEmail = request.session["email"]
        print ("You are logged in")
        print(userID)
        userHistory = ""
        # Search for user history in searchHistory hash table
            # Create history hash map for user if it does not exist
        if userID not in searchHistory:
                searchHistory[userID] = {}
        else:
            # Generate user history table code
            userHistory = create_history_table(searchHistory[userID])
        email = "<h6>Signed In as " + userEmail + "</h6>"
        return template('./views/signed_in_results.html', HistoryTable = userHistory, ResultsTable = "", Email= email, root ='./')
    print("You are not logged in")
    return template('./views/anonymous.html', root='./')

def get_search_results(search_key):
    rdb = redis.Redis()
    word_id = rdb.get('lexicon:' + search_key)
    docs = []
    if word_id:
        doc_ids = rdb.get('inverted_index:' + word_id).split(',')
        for doc_id in doc_ids:
            doc = []
            docID = doc_id.strip()
            doc.append(rdb.get('url:' + docID))
            doc.append(rdb.get('title:' + docID))
            doc.append(rdb.get('description:' + docID))
            doc.append(rdb.get('pagerank:' + docID))
            docs.append(doc)
        docs.sort(key=lambda x: x[3], reverse=True)
    return docs

# Function that gets called when a user hits Submit button
@route('/search', method="GET")
def count_words():
    # Get input string from input field and conver to lower case
    keywords = request.query.keywords
    #inputString = keywords.lower()

    # Local dictionary used to store keywords from current search
    worddict = {}

    if "id" in request.session:
        userID = request.session["id"]
        userEmail = request.session["email"]
        print(userEmail)
        print(request.session["logged_in"])

    '''
        Go through every word in the input string and check if it exists
        in the global searchHistory for the logged-in user dictionary and
        the local search keywords dictionary. If word exits, increment word count.
    '''
    inputWords = keywords.split()
    # search_key is the first word
    search_results = get_search_results(inputWords[0])
    # search_results = [["First", "Link0", "Desc0"],["second", "Link1", "Desc1"],["third", "Link2", "Desc2"],["fourth", "Link3", "Desc3"] ]
    for word in inputWords:
        if word in worddict:
            worddict[word] += 1
        else:
            worddict[word] = 1
        # If user is logged in, update user history
        if "logged_in" in request.session and request.session["logged_in"] is True:
            if word in searchHistory[userID]:
                searchHistory[userID][word] += 1
            else:
                searchHistory[userID][word] = 1
    # Generate search results html table
    table = create_results_table(worddict)

    # If user is logged in, create user history html table and return logged-in template
    if "logged_in" in request.session and request.session["logged_in"] is True:
        userHistoryTable = create_history_table(searchHistory[userID])
        email = "<h6>Signed In as " + userEmail + "</h6>"
        return template('./views/signed_in_results.html', ResultsTable=table, HistoryTable = userHistoryTable, Email = email)
    # If user is not logged in, return anonymous mode view
    return template('./views/anonymous_results.html', ResultsTable=table, p1=keywords, results=json.dumps(search_results))
# Function used to generate HTML results table
def create_results_table(word_dict):
    table = '\t<table class="table table-bordered" id="results">\n'
    top_words_sorted = sorted(word_dict, key=word_dict.get, reverse=True)
    for word in top_words_sorted:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t<td>" + str(word_dict[word]) + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table

# Function usedd to generate HTML search history table
def create_history_table(top_words):
    table = '\t<table class="table table-bordered" id="history">\n'
    top_words_sorted = sorted(top_words, key=top_words.get, reverse=True)
    for word in top_words_sorted[:10]:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t<td>" + str(top_words[word]) + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table

# Web app goes to this route when user clicks on "sign-in"
@route('/sign-in')
def home():
    flow = flow_from_clientsecrets("client_secrets.json", scope=SCOPE,
                                    redirect_uri=REDIRECT)
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

@route('/log-off')
def logoff():
    request.session["logged_in"] = False
    print("logout")
    request.session.delete()
    bottle.redirect("https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=" + HOME)

# Google redirects user to this route
@route('/redirect')
def redirect_page():
    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET, scope=SCOPE,
        redirect_uri=REDIRECT)
    credentials = flow.step2_exchange(code)
    token= credentials.id_token['sub']

    http = httplib2.Http()
    http = credentials.authorize(http)

    # Get user information
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    userEmail = user_document['email']
    userPhoto = user_document["picture"]

    # Store id, logged_in value and email in beaker session
    request.session["id"] = user_document["id"]
    request.session["logged_in"] = True
    request.session["email"] = userEmail

    userID = request.session["id"]

    request.session.save()
    bottle.redirect(HOME)


run(app=app_middleware, host='0.0.0.0', port=8080, debug=True, reoloader = True)
