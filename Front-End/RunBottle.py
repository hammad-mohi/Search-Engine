from bottle import route, run, get, post, request, static_file, template

@route('/')
def hello():
  return template('Main-Page.html',Table="", root='./')

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
        table = create_table(worddict)
        return template('Main-Page.html', Table=table)

def create_table(word_dict):
    table = '\t<table class="table table-bordered" id="results">\n'
    for word in word_dict:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t<td>" + str(word_dict[word]) + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table

run(host='localhost', port=8080, debug=True)
