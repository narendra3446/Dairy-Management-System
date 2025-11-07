from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# ✅ Use environment variable for safety; fallback to local MongoDB
app.config['MONGO_URI'] = os.environ.get(
    'MONGO_URI',
    'mongodb://localhost:27017/dairy_management_db'
)

# Initialize MongoDB
mongo = PyMongo(app)
db = mongo.db

# ✅ Collections (similar to tables)
users_col = db.users
products_col = db.products
orders_col = db.orders
order_items_col = db.order_items

# ✅ Helper function: create default admin user if not exists
def create_admin_user():
    admin = users_col.find_one({'username': 'admin'})
    if not admin:
        users_col.insert_one({
            'username': 'admin',
            'email': 'admin@dairy.com',
            'password': generate_password_hash('admin123'),
            'phone': '9999999999',
            'address': 'Dairy Management HQ',
            'is_admin': True,
            'created_at': datetime.utcnow()
        })
        print("✅ Default admin user created: admin / admin123")
    else:
        print("⚙️ Admin user already exists.")

# ✅ Sample route: Home
@app.route('/')
def home():
    products = list(products_col.find())
    return render_template('index.html', products=products)

# ✅ Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        phone = request.form['phone']
        address = request.form['address']

        # Check duplicate email or username
        if users_col.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or Email already exists!')
            return redirect(url_for('register'))

        users_col.insert_one({
            'username': username,
            'email': email,
            'password': password,
            'phone': phone,
            'address': address,
            'is_admin': False,
            'created_at': datetime.utcnow()
        })
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# ✅ Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_col.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)
            flash('Login successful!')
            return redirect(url_for('admin_dashboard') if user.get('is_admin') else url_for('home'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')

# ✅ Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

# ✅ Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        flash('Access denied!')
        return redirect(url_for('login'))
    users = list(users_col.find())
    products = list(products_col.find())
    return render_template('admin_dashboard.html', users=users, products=products)

# ✅ Initialize admin when starting app
with app.app_context():
    create_admin_user()

# ✅ Run app (Render-compatible)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
