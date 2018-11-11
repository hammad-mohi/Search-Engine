from crawler import crawler
from pagerank import page_rank
import redis

# Get crawler object and crawl on urls found in urls.txt
crawler = crawler(None, 'urls.txt')
crawler.crawl()
# Get the data structures generated by the crawler
lexicon = crawler.get_lexicon()
inverted_index = crawler.get_inverted_index()
resolved_inverted_index = crawler.get_resolved_inverted_index()
document_index = crawler.get_document_index()
# Run pagerank on the links generated by the crawler
pagerank = page_rank(crawler._links)
# Store data on persistent storage i.e. Redis
rdb = redis.Redis()
rdb.flushdb()

for word in lexicon:
    rdb.set('lexicon:' + str(word), lexicon[word])
for word_id in inverted_index:
    rdb.set('inverted_index:' + str(word_id), str(list(inverted_index[word_id])).strip('[]'))
for word in resolved_inverted_index:
    rdb.set('resolved_inverted_index:' + str(word), str(list(resolved_inverted_index[word])).strip('[]'))
for doc_id in document_index:
    doc = document_index[doc_id]
    rdb.set('url:' + str(doc_id), doc[0])
    rdb.set('title:' + str(doc_id), doc[1])
    rdb.set('description' + str(doc_id), doc[2])
    rdb.set('words:' + str(doc_id), doc[3])
for doc_id in pagerank:
    rdb.set('pagerank:' + str(doc_id), pagerank[doc_id])

"""for doc_id, rank in sorted(pagerank.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    document = crawler._document_index[doc_id]
    print str(doc_id) + "\n" + str(document[1]) + "\n" + str(document[0]) + "\n" + str(document[2]) + "\n= " + str(rank) + "\n"
    #print document[3]
"""
