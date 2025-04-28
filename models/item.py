from config import get_db_connection, ITEMS_COLLECTION
from bson.objectid import ObjectId
from datetime import datetime

class ItemModel:
    def __init__(self):
        self.db = get_db_connection()
        self.collection = self.db[ITEMS_COLLECTION]
    
    def create(self, name, description, quantity, price):
        """Create a new inventory item"""
        item = {
            'name': name,
            'description': description,
            'quantity': quantity,
            'price': price,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        result = self.collection.insert_one(item)
        return str(result.inserted_id)
    
    def get_all(self):
        """Get all inventory items"""
        items = list(self.collection.find().sort('name', 1))
        # Convert ObjectId to string for each item
        for item in items:
            item['_id'] = str(item['_id'])
        return items
    
    def get_by_id(self, item_id):
        """Get item by ID"""
        try:
            item = self.collection.find_one({'_id': ObjectId(item_id)})
            if item:
                item['_id'] = str(item['_id'])
            return item
        except:
            return None
    
    def update(self, item_id, name, description, quantity, price):
        """Update an existing item"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(item_id)},
                {'$set': {
                    'name': name,
                    'description': description,
                    'quantity': quantity,
                    'price': price,
                    'updated_at': datetime.now()
                }}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete(self, item_id):
        """Delete an item"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(item_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def update_quantity(self, item_id, quantity_change):
        """Update item quantity (add or subtract)"""
        try:
            item = self.get_by_id(item_id)
            if not item:
                return False
                
            new_quantity = item['quantity'] + quantity_change
            if new_quantity < 0:
                return False
                
            result = self.collection.update_one(
                {'_id': ObjectId(item_id)},
                {'$set': {'quantity': new_quantity, 'updated_at': datetime.now()}}
            )
            return result.modified_count > 0
        except:
            return False