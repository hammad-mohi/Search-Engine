from bottle import route, run, get, post, request, static_file, template
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
import bottle as app
from beaker.middleware import SessionMiddleware

# Beaker session options
session_opts={
    'session.type':'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto' : True
}

app_middleware = SessionMiddleware(app.app(), session_opts)
app_session = app.request.environ.get('beaker.session')

# Global dictionary used to store all searched keywords
keywords = {}
SCOPE = "https://www.googleapis.com/auth/userinfo.email"

@route('<filename:re:.*\.css>', name="static")
def css(filename):
    print ("css:" + filename)
    return static_file(filename, root='./', mimetype='text/css')

# Display main search engine page without showing any tables by default
@route('/')
def hello():
    session = app.request.environ.get('beaker.session')
    if session.get('logged_in'):
        print ("You are logged in")
        print(session["id"])
        email = str(session["email"])
        string = "<h1>" + email + "</>"
        return template('Logged-In.html', Email= string, ResultsTable="", HistoryTable = "", root ='./')
    print("You are not logged in")
    session.save()
    return template('Main-Page.html',ResultsTable="",root='./')

# Function that gets called when a user hits Submit button
@route('/', method="POST")
def count_words():
    session = app.request.environ.get('beaker.session') 
    # Get input string from input field and conver to lower case
    inputString = (request.forms.get('keywords')).lower()

    # Local dictionary used to store keywords from current search
    worddict = {}

    '''
        Go through every word in the input string and check if it exists
        in the global keywords dictionary and the local search keywords
        dictionary. If word exits, increment word count.
    '''
    for word in inputString.split():
        if word in worddict:
            worddict[word] += 1
        else:
            worddict[word] = 1
        if word in keywords:
            keywords[word] += 1
        else:
            keywords[word] = 1
    table = create_results_table(worddict)
    topWordsTable = create_history_table(keywords)
    # Reload main search page with results and search history tables
    return template('Main-Page.html', ResultsTable=table)

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
    for word in top_words_sorted[:20]:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t<td>" + str(top_words[word]) + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table


@route('/sign-in')
def home():
    session = app.request.environ.get('beaker.session')
    flow = flow_from_clientsecrets("client_secrets.json", scope=SCOPE,
                                    redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    app.redirect(str(uri))

@route('/log-off')
def logoff():
    session = app.request.environ.get('beaker.session')
    session["logged_in"] = False
    session.save()
    return template('Main-Page.html',ResultsTable="",root='./')

@route('/redirect')
def redirect_page():
    code = request.query.get('code', '')
    flow = OAuth2WebServerFlow(client_id="547443438769-9q9tatcnkpv6g05cj9d9ds98n0q661t1.apps.googleusercontent.com",
        client_secret="woMB_Z4XCZTyAW_-2hdUNpfx", scope=SCOPE,
        redirect_uri="http://localhost:8080/redirect")
    credentials = flow.step2_exchange(code)
    token= credentials.id_token['sub']
    print(token)

    http = httplib2.Http()
    http = credentials.authorize(http)

    # Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    print(user_document)
    user_email = user_document['email']
    photo = user_document["picture"]

    session = app.request.environ.get('beaker.session')
    session["id"] = user_document["id"]
    session["logged_in"] = True
    session["email"] = user_email
    string = "<h1>" + user_email + "</>"
    #string = "<img src=" + photo + ">"
    session.save()
    return template('Logged-In.html', Email = string,  ResultsTable="", HistoryTable="",root='./')


run(app=app_middleware, host='localhost', port=8080, debug=True, reoloader = True)


'''
 @Routes
   - Load page (Check if user is signed in or create a new session)
               (Return the appropriate page)'''
