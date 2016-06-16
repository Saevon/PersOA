from pymongo import MongoClient

URI = "mongodb://127.0.0.1:27019"
client = MongoClient(URI)

db = client.test
db.people.insert_one({
    'name': 'Bob',
    'title': 'Producer',
})

cursor = db.restaurants.find()
for document in cursor:
    print(document)
