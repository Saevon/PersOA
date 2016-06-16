from pymongo import MongoClient

URI = "mongodb://database:27019"
client = MongoClient(URI)

db = client.test
db.people.insert_one({
    'name': 'Bob',
    'title': 'Producer',
})

cursor = db.restaurants.find()
for document in cursor:
    print(document)
