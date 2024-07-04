from pymongo import MongoClient

client = MongoClient(
            'mongodb+srv://python:pythonpass@datacluster.8ohor.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.get_database('RDP_DB')


collection = db.irins

result_fields = {'name':1, 'qual':1, 'cite':1, 'hindex':1, 'orcid':1, 'link':1,'_id':1}

search_terms = "machine learning".split()
query = {'exp': {'$all': search_terms}}

res = collection.find(query, result_fields)
print(len(list(res)))