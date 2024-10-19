from pymongo import MongoClient

# Replace the URL with your MongoDB connection string
client = MongoClient('localhost', 27017)

# Access the database
db = client['my_database']

# Access a collection
collection = db['my_collection']

# Example: Insert a document
collection.insert_one({'name': 'John Doe', 'age': 30})

# Example: Query the collection
for doc in collection.find():
    print(doc)
