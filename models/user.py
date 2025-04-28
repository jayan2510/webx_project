from config import get_db_connection, USERS_COLLECTION
from bson.objectid import ObjectId
from datetime import datetime
import hashlib
import os

class UserModel:
    def __init__(self):
        self.db = get_db_connection()
        self.collection = self.db[USERS_COLLECTION]
    
    def _hash_password(self, password, salt=None):
        """Hash a password with salt for secure storage"""
        if salt is None:
            salt = os.urandom(32)  # Generate a new salt
        
        # Hash password with salt
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # Number of iterations
        )
        
        return {'salt': salt, 'key': key}
    
    def create(self, username, password):
        """Create a new user"""
        # Check if username already exists
        if self.get_by_username(username):
            return None
        
        # Hash the password
        password_hash = self._hash_password(password)
        
        user = {
            'username': username,
            'password_hash': password_hash['key'],
            'salt': password_hash['salt'],
            'created_at': datetime.now()
        }
        
        result = self.collection.insert_one(user)
        return str(result.inserted_id)
    
    def authenticate(self, username, password):
        """Authenticate a user with username and password"""
        user = self.get_by_username(username)
        
        if not user:
            return None
        
        # Get stored salt
        salt = user['salt']
        
        # Hash the provided password with the stored salt
        password_hash = self._hash_password(password, salt)
        
        # Compare password hashes
        if password_hash['key'] == user['password_hash']:
            return user
        
        return None
    
    def get_by_username(self, username):
        """Get user by username"""
        user = self.collection.find_one({'username': username})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    def get_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.collection.find_one({'_id': ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except:
            return None