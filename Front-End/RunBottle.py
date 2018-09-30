from bottle import route, run, get, post, request, static_file, template
from collections import OrderedDict

keywords = {}

@route('/')
def hello():
  return template('Main-Page.html',ResultsTable="", HistoryTable="" ,root='./')

@route('/', method="POST")
def count_words():
    inputString = (request.forms.get('keywords')).lower()
    worddict = {}
    if(len(inputString) == 0):
        return "Empty"
    else:
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
        return template('Main-Page.html', ResultsTable=table, HistoryTable=topWordsTable)

def create_results_table(word_dict):
    table = '\t<table class="table table-bordered" id="results">\n'
    for word in word_dict:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t<td>" + str(word_dict[word]) + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table

def create_history_table(top_words):
    table = '\t<table class="table table-bordered" id="history">\n'
    top_words_sorted = sorted(top_words, key=top_words.get, reverse=True)
    for word in top_words_sorted[:20]:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table

run(host='localhost', port=8080, debug=True)
