import redis
import pymongo
from fuzzywuzzy import fuzz, process

# Queries redis/ mongodb for search results and returns search results dictionary
def get_word_search_results(search_key):
    '''myclient = pymongo.MongoClient("mongodb://Deep297:seek-search3@ds111244.mlab.com:11244/seek_search-engine")
    db = myclient["seek_search-engine"]
    lexicon = db["lexicons"]
    print(lexicon)
    inverted_index = db["inverted_index"]
    documents = db["documents"]
    docs = []
    word_id = lexicon.distinct(search_key)
    if(word_id):
     doc_ids = inverted_index.distinct(str(word_id[0]))
     doc_ids = doc_ids[0][5:-2]
     for item in list(doc_ids.split(',')):
         doc_t = []
         info = list(documents.distinct(item.strip()))
         for item in info:
             doc_t.append(item)
         docs.append(doc_t)
     docs.sort(key=lambda x: x[0], reverse=False)
    return docs'''
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

# Given an input string of words, return search results
def get_combined_results(inputWords):
    inputLen = len(inputWords)
    if inputLen == 0:
            return none
    elif inputLen == 1:
        return get_word_search_results(inputWords[0])
    else:
        # Get serach results for the first two words in the search string
        word1_results = get_word_search_results(inputWords[0])
        word2_results = get_word_search_results(inputWords[1])
        # Make a list of the common and non common search results from both words
        combinedResults = intersection(word1_results, word2_results)
        nonCommonResults = difference(word1_results, combinedResults) + difference(word2_results, combinedResults)
        # If there were no common results, return both results sorted by pagerank
        if len(combinedResults) == 0:
            return (word1_results + word2_results)
        # Return list with common results at the beginning and noncommon results at the end
        else:
            return combinedResults + nonCommonResults



# Creates HTML elements for the search results
def create_result_elements(search_results):
    results = ""
    for docs in search_results:
        # if (len(item) == 4):
        results += "<div class='blurred-box'>"
        results += "    <a class='result-title' href='"+ docs[0] + "'>" + docs[1] + "</a>"
        results += "    <p class='result-link'>" + docs[0] + "</p>"
        results += "    <hr class='result-separator'>"
        results += "    <p class='result-desc'>" + docs[2] + "</p>"
        results += "</div>"
    return results

# Checks to see if search string is a mathematical expression. If it is, return html string for the answer
def check_math_expression(search_string):
    try:
        test_math = eval(search_string)
    except(ValueError, NameError, SyntaxError, TypeError, ZeroDivisionError):
        return ""
    result = ""
    if test_math is not None:
        result += "<div class='blurred-box'>"
        result += "    <p class='result-title'>" + search_string + " = </p>"
        result += "    <p class='result-desc'>" + str(test_math) + "</p>"
        result += "</div>"
        return result

def guessInput(inputWords):
    #TODO: REPLACE WITH LIST OF WORDS
    choices = getWordArray()
    ClosestWord = process.extractOne(inputWords[0], choices)
    print(ClosestWord)
    redirect = ""
    if ClosestWord is not None:
        redirect += "<h2 id=error-redirect> Did You Mean:"
        redirect += "    <a href='http://localhost:8080/search?keywords=" + ClosestWord[0] + "'>" + ClosestWord[0] + "</a></h2>"
    return redirect

def getWordArray():
    rdb = redis.Redis()
    wordArray = rdb.get('all_words').split(",")
    return wordArray



# Return list containing there common elements of the two input lists
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# Return list containing the non-common elements of the two input lists
def difference(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3
