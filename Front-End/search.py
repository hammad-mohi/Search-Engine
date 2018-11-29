import redis
import pymongo

# Queries redis/ mongodb for search results and returns search results dictionary
def get_word_search_results(search_key):
    myclient = pymongo.MongoClient("mongodb://Deep297:seek-search3@ds111244.mlab.com:11244/seek_search-engine")
    db = myclient["seek_search-engine"]
    lexicon = db["lexicons"]
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
    return docs
    '''rdb = redis.Redis()
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
    return docs'''

def get_combined_results(inputWords):
    inputLen = len(inputWords)
    if inputLen == 0:
            return none
    elif inputLen == 1:
        return get_word_search_results(inputWords[0])
    else:
        word1_results = get_word_search_results(inputWords[0])
        word2_results = get_word_search_results(inputWords[1])
        print ("Len1: " + str(len(word1_results)) + " , Len2: " + str(len(word2_results)))
        combinedResults = intersection(word1_results, word2_results)
        print("Combined Len: " + str(len(combinedResults)))
        if len(combinedResults) == 0:
            return (word1_results + word2_results)
        else:
            return combinedResults



# Creates HTML elements for the search results
def create_result_elements(search_results):
    results = ""
    for item in search_results:
        if (len(item) == 4):
            results += "<div class = 'blurred-box' style='max-width: 55rem'>"
            results += "    <h4 class = 'result-title'> " + item[1] + "</h4>"
            results += "    <a class = 'result-link' href='" + item[3] + "' target='_blank'>" + item[3] + "</a>"
            results += "   <h1 class = 'result-desc'> " + item[2] + "</h1>"
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
        result += "<div class = 'blurred-box' style='max-width: 55rem'>"
        result += "    <h4 class = 'result-title'> " + search_string + " = </h4>"
        result += "   <h1 class = 'result-desc'> " + str(test_math) + "</h1>"
        result += "</div>"
        return result

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
