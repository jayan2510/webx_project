import os
from pymongo import MongoClient

# MongoDB Connection Settings
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'inventory_management')

# Connect to MongoDB
def get_db_connection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db

# Collection names
USERS_COLLECTION = 'users'
ITEMS_COLLECTION = 'items'