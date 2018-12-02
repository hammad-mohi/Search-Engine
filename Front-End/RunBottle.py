import json
import bottle
import httplib2
from search import *
from fuzzywuzzy import process
from collections import defaultdict
from apiclient.discovery import build
from googleapiclient.errors import HttpError
from beaker.middleware import SessionMiddleware
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from bottle import route, run, get, post, request, static_file, template, error



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
wordList = json.dumps(getWordList())

# Retrieve beaker session before every route
@bottle.hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

# Route used to service .css file requests
@route('<filename:re:.*\.css>', name="static")
def css(filename):
    print ("css:" + filename)
    return static_file(filename, root='./')

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
@error(400)
@error(401)
@error(402)
@error(403)
@error(404)
@error(500)
def error404(error):
    return template('./views/error.html',
                    Error_Message = "Oops something went wrong",
                    Redirect = "",
                    root='./')

# Display main search engine page without showing any tables by default
@route('/')
def home():
    # Check if user is logged in
    if "logged_in" in request.session and request.session["logged_in"] is True:
        userID = request.session["id"]
        userEmail = request.session["email"]
        userName = request.session["name"]
        userPhoto = request.session["photo"]
        print ("You are logged in")
        userHistory = ""
        # Search for user history in searchHistory hash table
            # Create history hash map for user if it does not exist
        if userID not in searchHistory:
                searchHistory[userID] = {}
        else:
            return template('./views/signed_in.html',
                            Email= userEmail,
                            Name = userName,
                            Photo = userPhoto,
                            wordList = wordList,
                            root ='./')

    print("You are not logged in")
    return template('./views/anonymous.html',
                    wordList = wordList,
                    root='./')   

# Function that gets called when a user hits Submit button
@route('/search', method="GET")
def search():
    # Get input string from input field and conver to lower case
    keywords = request.query.keywords
    inputString = keywords.lower()
    inputWords = inputString.split()

    if "id" in request.session:
        userID = request.session["id"]
        userEmail = request.session["email"]
        userName = request.session["name"]
        userPhoto = request.session["photo"]
        print(userEmail)
        print(request.session["logged_in"])

    if(len(inputWords) > 0):
        search_results = get_combined_results(inputWords)
        resultsLen = len(search_results)
    else:
        return template('./views/error.html',
                        Error_Message = "No results found.",
                        Redirect = "",
                        root='./')

    if (resultsLen == 0):
        math_expression_result = check_math_expression(keywords)
        if(math_expression_result != ""):
                return template('./views/anonymous_results.html',
                                p1=keywords,
                                results = math_expression_result,
                                numResults = 1,
                                wordList = wordList)
        else:
            redirect = guessInput(inputWords)
            return template('./views/error.html',
                            Error_Message = "No results found for " + inputString + " .",
                            Redirect = redirect,
                            root='./')

    result_elements = create_result_elements(search_results)
    # If user is logged in, update user history
    if "logged_in" in request.session and request.session["logged_in"] is True:
        if inputString in searchHistory[userID]:
            searchHistory[userID][inputString] += 1
        else:
            searchHistory[userID][inputString] = 1
        print searchHistory[userID]
    # If user is logged in, create user history html table and return logged-in template
    if "logged_in" in request.session and request.session["logged_in"] is True:
        return template('./views/signed_in_results.html',
                        Email = userEmail,
                        Name = userName,
                        Photo = userPhoto,
                        p1=keywords,
                        results=result_elements,
                        numResults = resultsLen,
                        wordList = wordList)
    # If user is not logged in, return anonymous mode view
    return template('./views/anonymous_results.html',
                    p1 = keywords,
                    results = result_elements,
                    numResults = resultsLen,
                    wordList= wordList)

# Web app goes to this route when user clicks on "sign-in"
@route('/sign-in')
def login():
    flow = flow_from_clientsecrets("client_secrets.json",
                                    scope=SCOPE,
                                    redirect_uri=REDIRECT)
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

@route('/log-off')
def logoff():
    request.session["logged_in"] = False
    print("logout")
    request.session.delete()
    bottle.redirect(HOME)

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
    print user_document
    userEmail = user_document['email']
    try:
        userName = user_document['name']
    except KeyError:
        userName = ""
    userPhoto = user_document["picture"]

    # Store id, email, name, photo and logged_in value in beaker session
    request.session["id"] = user_document["id"]
    request.session["logged_in"] = True
    request.session["email"] = userEmail
    request.session["name"] = userName
    request.session["photo"] = userPhoto

    userID = request.session["id"]
    request.session.save()
    bottle.redirect(HOME)


run(app=app_middleware, host='0.0.0.0', port=8080, debug=True, reoloader = True)
