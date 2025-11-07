"""
Dairy Management System - Complete Application
A full-featured dairy management web application built with Flask and SQLite
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dairy-management-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dairy_management.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(50), default='Liter')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='product', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'unit': self.unit,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.DateTime)
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()
    
    # Check if admin user exists, if not create default data
    if User.query.filter_by(username='admin').first() is None:
        print("Initializing default admin user and sample products...")
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@dairymanagement.com',
            password=generate_password_hash('admin123'),
            phone='9999999999',
            address='Dairy Management HQ',
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.flush()
        
        # Create sample products
        sample_products = [
            Product(name='Milk (1L)', description='Fresh whole milk', price=50, stock=100, unit='Liter'),
            Product(name='Yogurt (500ml)', description='Creamy yogurt', price=80, stock=75, unit='ml'),
            Product(name='Buttermilk (1L)', description='Fresh buttermilk', price=40, stock=50, unit='Liter'),
            Product(name='Paneer (500g)', description='Fresh cottage cheese', price=250, stock=30, unit='grams'),
            Product(name='Ghee (500ml)', description='Pure clarified butter', price=500, stock=20, unit='ml'),
            Product(name='Cheese (200g)', description='Processed cheese', price=150, stock=40, unit='grams'),
        ]
        for product in sample_products:
            db.session.add(product)
        
        db.session.commit()
        print("Default admin user and sample products created successfully!")
    else:
        print("Database already initialized with data")

# ==================== DECORATORS ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('user_dashboard') if user else url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if not all([username, email, password, phone, address]):
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            phone=phone,
            address=address,
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# ==================== USER ROUTES ====================

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    user = User.query.get(session['user_id'])
    if user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    products = Product.query.filter(Product.stock > 0).all()
    products_dict = [p.to_dict() for p in products]
    return render_template('user_dashboard.html', products=products_dict, user=user)

@app.route('/user/place-order', methods=['POST'])
@login_required
def place_order():
    data = request.get_json()
    items = data.get('items', [])
    
    if not items:
        return jsonify({'success': False, 'message': 'No items selected'}), 400

    total_amount = 0
    order_items_list = []

    for item in items:
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 400
        if product.stock < item['quantity']:
            return jsonify({'success': False, 'message': f'Insufficient stock for {product.name}'}), 400
        
        subtotal = product.price * item['quantity']
        total_amount += subtotal
        order_items_list.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal
        })

    # Create order
    new_order = Order(
        user_id=session['user_id'],
        total_amount=total_amount,
        status='Pending',
        delivery_date=datetime.utcnow() + timedelta(days=1)
    )
    db.session.add(new_order)
    db.session.flush()

    # Add order items and update stock
    for item in order_items_list:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item['product'].id,
            quantity=item['quantity'],
            price=item['product'].price,
            subtotal=item['subtotal']
        )
        item['product'].stock -= item['quantity']
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Order placed successfully', 'order_id': new_order.id})

@app.route('/user/orders')
@login_required
def user_orders():
    user = User.query.get(session['user_id'])
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.order_date.desc()).all()
    return render_template('user_orders.html', orders=orders, user=user)

@app.route('/user/receipt/<int:order_id>')
@login_required
def user_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != session['user_id']:
        flash('Unauthorized', 'danger')
        return redirect(url_for('user_dashboard'))
    return render_template('receipt.html', order=order)

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_products = Product.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html', 
                         total_products=total_products,
                         total_users=total_users,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@app.route('/admin/products')
@admin_required
def admin_products():
    products = Product.query.all()
    return render_template('admin_products.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0')
        stock = request.form.get('stock', '0')
        unit = request.form.get('unit', 'Liter')

        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            flash('Invalid price or stock value', 'danger')
            return redirect(url_for('add_product'))

        if not name:
            flash('Product name is required', 'danger')
            return redirect(url_for('add_product'))

        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            unit=unit
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin_products'))
    return render_template('add_product.html')

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        try:
            product.price = float(request.form.get('price', product.price))
            product.stock = int(request.form.get('stock', product.stock))
        except ValueError:
            flash('Invalid price or stock value', 'danger')
            return redirect(url_for('edit_product', product_id=product_id))
        product.unit = request.form.get('unit', 'Liter')
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin_products'))
    return render_template('edit_product.html', product=product)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/order/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status', 'Pending')
    if status in ['Pending', 'Completed', 'Cancelled']:
        order.status = status
        db.session.commit()
        flash('Order status updated', 'success')
    else:
        flash('Invalid status', 'danger')
    return redirect(url_for('admin_orders'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/reports')
@admin_required
def admin_reports():
    orders = Order.query.all()
    products = Product.query.all()
    
    daily_sales = {}
    for order in orders:
        date = order.order_date.date()
        daily_sales[date] = daily_sales.get(date, 0) + order.total_amount
    
    return render_template('admin_reports.html', 
                         daily_sales=daily_sales,
                         products=products,
                         orders=orders)

@app.route('/admin/reset-password', methods=['GET', 'POST'])
@admin_required
def admin_reset_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        user = User.query.get(session['user_id'])
        
        if not check_password_hash(user.password, old_password):
            flash('Old password is incorrect', 'danger')
            return redirect(url_for('admin_reset_password'))
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('admin_reset_password'))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('admin_reset_password'))
        
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password changed successfully! Please login again.', 'success')
        return redirect(url_for('logout'))
    
    return render_template('admin_reset_password.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    debug = os.environ.get('ENV') != 'production'
    port = int(os.environ.get('PORT', 5000))
    # Only run if not using Gunicorn (development only)
    if 'gunicorn' not in os.environ.get('SERVER_SOFTWARE', ''):
        app.run(debug=debug, host='0.0.0.0', port=port)
