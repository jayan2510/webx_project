from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import os
from models.item import ItemModel
from models.user import UserModel
from utils.auth import login_required

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and session

# Initialize models
item_model = ItemModel()
user_model = UserModel()

# Routes for authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = user_model.authenticate(username, password)
        if user:
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('login.html', register=True)
        
        if user_model.get_by_username(username):
            flash('Username already exists', 'danger')
            return render_template('login.html', register=True)
        
        user_model.create(username, password)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('login.html', register=True)

# Routes for inventory management
@app.route('/')
@login_required
def index():
    items = item_model.get_all()
    return render_template('index.html', items=items)

@app.route('/item/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = int(request.form.get('quantity'))
        price = float(request.form.get('price'))
        
        item_model.create(name, description, quantity, price)
        flash('Item added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', item=None, action='Add')

@app.route('/item/edit/<item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = item_model.get_by_id(item_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = int(request.form.get('quantity'))
        price = float(request.form.get('price'))
        
        item_model.update(item_id, name, description, quantity, price)
        flash('Item updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', item=item, action='Edit')

@app.route('/item/delete/<item_id>')
@login_required
def delete_item(item_id):
    item_model.delete(item_id)
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)