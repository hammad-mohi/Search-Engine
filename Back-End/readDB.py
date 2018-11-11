import redis

r = redis.Redis()

print r.get('lexicon:toronto')
#print r.get('inverted_index:5')
#print r.get('resolved_inverted_index:toronto')
print r.get('url:516')
print r.get('title:516')
print r.get('description:516')
#print r.get('words:1')
print r.get('pagerank:516')
