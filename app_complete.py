"""
Dairy Management System - MongoDB version (MongoDB-safe)
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
import secrets
from dotenv import load_dotenv
load_dotenv()


# Initialize Flask app
app = Flask(__name__)

ENV = os.getenv("ENV", "development")

if ENV == "production":
    app.config["MONGO_URI"] = os.getenv("MONGO_URI") 
else:
    app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/dairy_management_db"
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dairy-management-secret-key-2025')

app.config['JSON_SORT_KEYS'] = False
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') in ['True', 'true', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@dairymanagement.com')

# Initialize Mail and PyMongo
mail = Mail(app)
mongo_client = PyMongo(app)
db = mongo_client.db  # shorthand


# ----------------- Helpers -----------------

def objid_to_str(doc):
    """Convert _id ObjectId to string for jsonify/template use."""
    if not doc:
        return None
    doc['_id'] = str(doc['_id'])
    return doc


def convert_products_cursor(cursor):
    out = []
    for p in cursor:
        p['_id'] = str(p['_id'])
        # keep created_at serializable
        if 'created_at' in p and isinstance(p['created_at'], datetime):
            p['created_at'] = p['created_at'].isoformat()
        out.append(p)
    return out


def get_user_by_id(user_id_str):
    try:
        return db.users.find_one({"_id": ObjectId(user_id_str)})
    except Exception:
        return None


def get_user_by_email(email):
    return db.users.find_one({"email": email})


# ----------------- Initialization (one-time) -----------------

@app.before_request
def initialize_db():
    """
    Creates an init flag in Mongo and a default admin + sample products the first time.
    Safe to run repeatedly — it checks existence and won't duplicate.
    """
    try:
        init_flag = db.init_flags.find_one({})
        if not init_flag:
            db.init_flags.insert_one({"initialized": False, "created_at": datetime.now(timezone.utc)})
            init_flag = db.init_flags.find_one({})

        if not init_flag.get("initialized", False):
            admin_email = 'admin@dairymanagement.com'
            if not db.users.find_one({"email": admin_email}):
                print("Initializing default admin user and sample products...")

                admin_user = {
                    "username": "admin",
                    "email": admin_email,
                    "password": generate_password_hash("admin123"),
                    "phone": "9999999999",
                    "address": "Dairy Management HQ",
                    "is_admin": True,
                    "created_at": datetime.now(timezone.utc),
                    "reset_token": None,
                    "reset_token_expiry": None
                }
                db.users.insert_one(admin_user)

                sample_products = [
                    {"name": "Milk (1L)", "description": "Fresh whole milk", "price": 50.0, "stock": 100, "unit": "Liter", "created_at": datetime.now(timezone.utc)},
                    {"name": "Yogurt (500ml)", "description": "Creamy yogurt", "price": 80.0, "stock": 75, "unit": "ml", "created_at": datetime.now(timezone.utc)},
                    {"name": "Buttermilk (1L)", "description": "Fresh buttermilk", "price": 40.0, "stock": 50, "unit": "Liter", "created_at": datetime.now(timezone.utc)},
                    {"name": "Paneer (500g)", "description": "Fresh cottage cheese", "price": 250.0, "stock": 30, "unit": "grams", "created_at": datetime.now(timezone.utc)},
                    {"name": "Ghee (500ml)", "description": "Pure clarified butter", "price": 500.0, "stock": 20, "unit": "ml", "created_at": datetime.now(timezone.utc)},
                    {"name": "Cheese (200g)", "description": "Processed cheese", "price": 150.0, "stock": 40, "unit": "grams", "created_at": datetime.now(timezone.utc)},
                ]
                db.products.insert_many(sample_products)

            db.init_flags.update_one({"_id": init_flag["_id"]}, {"$set": {"initialized": True, "updated_at": datetime.now(timezone.utc)}})
            print("Default admin user and sample products created successfully!")
    except Exception as e:
        print(f"Initialization error: {str(e)}")


# ----------------- Decorators -----------------

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
        user = get_user_by_id(session['user_id'])
        if not user or not user.get('is_admin', False):
            flash('Admin access required', 'danger')
            return redirect(url_for('user_dashboard') if user else url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ----------------- Auth routes -----------------

@app.route('/')
def index():
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        if user and user.get('is_admin'):
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

        if db.users.find_one({"username": username}):
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        if db.users.find_one({"email": email}):
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))

        new_user = {
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "phone": phone,
            "address": address,
            "is_admin": False,
            "created_at": datetime.now(timezone.utc),
            "reset_token": None,
            "reset_token_expiry": None
        }
        db.users.insert_one(new_user)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = db.users.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)
            flash('Login successful!', 'success')
            if user.get('is_admin', False):
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


# ----------------- User routes -----------------

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    user = get_user_by_id(session['user_id'])
    if user and user.get('is_admin'):
        return redirect(url_for('admin_dashboard'))

    products_cursor = db.products.find({"stock": {"$gt": 0}})
    products = convert_products_cursor(products_cursor)
    return render_template('user_dashboard.html', products=products, user=user)


@app.route('/user/place-order', methods=['POST'])
@login_required
def place_order():
    data = request.get_json()
    items = data.get('items', [])

    if not items:
        return jsonify({'success': False, 'message': 'No items selected'}), 400

    total_amount = 0.0
    order_items = []

    # Validate items and compute totals
    for item in items:
        try:
            prod = db.products.find_one({"_id": ObjectId(item['product_id'])})
        except Exception:
            return jsonify({'success': False, 'message': 'Invalid product id'}), 400
        if not prod:
            return jsonify({'success': False, 'message': 'Product not found'}), 400
        if prod.get('stock', 0) < int(item['quantity']):
            return jsonify({'success': False, 'message': f"Insufficient stock for {prod['name']}"}), 400

        subtotal = float(prod['price']) * float(item['quantity'])
        total_amount += subtotal
        order_items.append({
            "product_id": prod['_id'],            # stored as ObjectId
            "product_name": prod['name'],
            "product_unit": prod.get('unit', ''),
            "quantity": int(item['quantity']),
            "price": float(prod['price']),
            "subtotal": subtotal
        })

    # Create order (store under 'order_items' — consistent across templates)
    order_doc = {
        "user_id": ObjectId(session['user_id']),
        "total_amount": total_amount,
        "status": "Pending",
        "order_date": datetime.now(timezone.utc),
        "delivery_date": datetime.now(timezone.utc) + timedelta(days=1),
        "order_items": order_items
    }
    order_result = db.orders.insert_one(order_doc)

    db.users.update_one(
    {"_id": ObjectId(session['user_id'])},
    {"$inc": {"total_orders": 1}}
)


    # Update product stock (decrement)
    for it in order_items:
        db.products.update_one({"_id": it['product_id']}, {"$inc": {"stock": -int(it['quantity'])}})

    return jsonify({'success': True, 'message': 'Order placed successfully', 'order_id': str(order_result.inserted_id)})


@app.route('/user/orders')
@login_required
def user_orders():
    user = get_user_by_id(session['user_id'])
    orders_cursor = db.orders.find({"user_id": ObjectId(session['user_id'])}).sort("order_date", -1)
    orders = []
    for o in orders_cursor:
        o['_id'] = str(o['_id'])
        # Ensure order_items exists and convert inner ObjectIds to strings for template convenience
        if o.get('order_items') is None:
            o['order_items'] = []
        for it in o['order_items']:
            if isinstance(it.get('product_id'), ObjectId):
                it['product_id'] = str(it['product_id'])
        # Leave datetimes as datetimes so Jinja's strftime works.
        # If they are strings (older orders), try to parse ISO format
        if isinstance(o.get('order_date'), str):
            try:
                o['order_date'] = datetime.fromisoformat(o['order_date'])
            except:
                pass
        if isinstance(o.get('delivery_date'), str) and o['delivery_date']:
            try:
                o['delivery_date'] = datetime.fromisoformat(o['delivery_date'])
            except:
                pass
        orders.append(o)
    return render_template('user_orders.html', orders=orders, user=user)


@app.route('/user/receipt/<order_id>')
@login_required
@app.route("/receipt/<order_id>")
def user_receipt(order_id):
    try:
        order = db.orders.find_one({"_id": ObjectId(order_id)})
    except Exception:
        flash('Invalid order', 'danger')
        return redirect(url_for('user_orders'))

    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('user_orders'))

    # Ensure User owns the order
    if str(order['user_id']) != session.get('user_id'):
        flash('Unauthorized access', 'danger')
        return redirect(url_for('user_orders'))

    # Convert for template
    order['_id'] = str(order['_id'])

    # Ensure order_items exists
    order['order_items'] = order.get('order_items', [])

    # Parse product_id for template
    for it in order['order_items']:
        if isinstance(it.get('product_id'), ObjectId):
            it['product_id'] = str(it['product_id'])

    # Convert timestamps
    if isinstance(order.get('order_date'), str):
        try:
            order['order_date'] = datetime.fromisoformat(order['order_date'])
        except:
            order['order_date'] = datetime.now()

    if isinstance(order.get('delivery_date'), str):
        try:
            order['delivery_date'] = datetime.fromisoformat(order['delivery_date'])
        except:
            pass

    return render_template("receipt.html", order=order)



# ----------------- Admin routes -----------------

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_products = db.products.count_documents({})
    total_users = db.users.count_documents({"is_admin": False})
    total_orders = db.orders.count_documents({})
    # total revenue using aggregation
    agg = db.orders.aggregate([{"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}])
    total_revenue = 0.0
    for r in agg:
        total_revenue = r.get('total', 0.0)

    recent_orders_cursor = db.orders.find().sort("order_date", -1).limit(10)
    recent_orders = []
    for o in recent_orders_cursor:
        o['_id'] = str(o['_id'])

        # Attach user dict (if available)
        user = None
        try:
            # order['user_id'] is an ObjectId in DB; handle string/objid safely
            user_obj = o.get('user_id')
            if isinstance(user_obj, ObjectId):
                user = db.users.find_one({"_id": user_obj})
            else:
                # attempt to convert string id to ObjectId
                try:
                    user = db.users.find_one({"_id": ObjectId(str(user_obj))})
                except:
                    user = None
        except Exception:
            user = None

        if user:
            user['_id'] = str(user['_id'])
            # keep only safe fields
            o['user'] = {
                "username": user.get('username', 'Unknown'),
                "email": user.get('email', ''),
                "phone": user.get('phone', '')
            }
        else:
            o['user'] = None

        # Try to keep order_date as datetime for template strftime
        if isinstance(o.get('order_date'), str):
            try:
                o['order_date'] = datetime.fromisoformat(o['order_date'])
            except:
                pass

        recent_orders.append(o)

    return render_template('admin_dashboard.html',
                           total_products=total_products,
                           total_users=total_users,
                           total_orders=total_orders,
                           total_revenue=total_revenue,
                           recent_orders=recent_orders)


@app.route('/admin/products')
@admin_required
def admin_products():
    products_cursor = db.products.find()
    products = convert_products_cursor(products_cursor)
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

        new_product = {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "unit": unit,
            "created_at": datetime.now(timezone.utc)
        }
        db.products.insert_one(new_product)
        flash('Product added successfully', 'success')
        return redirect(url_for('admin_products'))
    return render_template('add_product.html')


@app.route('/admin/product/edit/<product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})
    except Exception:
        flash('Invalid product id', 'danger')
        return redirect(url_for('admin_products'))

    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('admin_products'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        try:
            price = float(request.form.get('price', product['price']))
            stock = int(request.form.get('stock', product['stock']))
        except ValueError:
            flash('Invalid price or stock value', 'danger')
            return redirect(url_for('edit_product', product_id=product_id))
        unit = request.form.get('unit', 'Liter')

        db.products.update_one({"_id": product['_id']}, {"$set": {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "unit": unit
        }})
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin_products'))

    # prepare product for template
    product['_id'] = str(product['_id'])
    if isinstance(product.get('created_at'), datetime):
        product['created_at'] = product['created_at'].isoformat()
    return render_template('edit_product.html', product=product)


@app.route('/admin/product/delete/<product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    try:
        db.products.delete_one({"_id": ObjectId(product_id)})
        flash('Product deleted successfully', 'success')
    except Exception:
        flash('Invalid product id', 'danger')
    return redirect(url_for('admin_products'))


@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders_cursor = db.orders.find().sort("order_date", -1)
    orders = []

    for o in orders_cursor:
        o['_id'] = str(o['_id'])
        o['user_id'] = str(o['user_id'])

        # Convert dates
        if isinstance(o.get('order_date'), datetime):
            pass
        elif isinstance(o.get('order_date'), str):
            try:
                o['order_date'] = datetime.fromisoformat(o['order_date'])
            except:
                o['order_date'] = datetime.now()

        # 🟩 FIX: ensure order_items exists
        o['order_items'] = o.get('order_items', [])

        # Fetch user info
        user = db.users.find_one({"_id": ObjectId(o['user_id'])})
        if user:
            user['_id'] = str(user['_id'])
        o['user_data'] = user

        orders.append(o)

    return render_template('admin_orders.html', orders=orders)



@app.route('/admin/order/<order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    status = request.form.get('status', 'Pending')
    if status not in ['Pending', 'Completed', 'Cancelled']:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin_orders'))
    try:
        db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status}})
        flash('Order status updated', 'success')
    except Exception:
        flash('Invalid order id', 'danger')
    return redirect(url_for('admin_orders'))


@app.route('/admin/users')
@admin_required
def admin_users():
    users = list(db.users.find())
    # Convert string timestamps to datetime objects (safe conversion)
    for user in users:
        created_at = user.get("created_at")
        if isinstance(created_at, str):
            try:
                user["created_at"] = datetime.fromisoformat(created_at)
            except ValueError:
                try:
                    user["created_at"] = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
    return render_template('admin_users.html', users=users)


@app.route('/admin/reports')
@admin_required
def admin_reports():
    orders_cursor = db.orders.find()
    products_cursor = db.products.find()

    # daily sales
    daily_sales = {}
    for order in orders_cursor:
        date = order['order_date'].date() if isinstance(order.get('order_date'), datetime) else None
        if date:
            daily_sales[date] = daily_sales.get(date, 0) + float(order.get('total_amount', 0))

    products = convert_products_cursor(products_cursor)
    return render_template('admin_reports.html',
                           daily_sales=daily_sales,
                           products=products,
                           orders=list(db.orders.find()))


@app.route('/admin/reset-password', methods=['GET', 'POST'])
@admin_required
def admin_reset_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        user = get_user_by_id(session['user_id'])
        if not user or not check_password_hash(user['password'], old_password):
            flash('Old password is incorrect', 'danger')
            return redirect(url_for('admin_reset_password'))

        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('admin_reset_password'))

        if len(new_password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('admin_reset_password'))

        db.users.update_one({"_id": ObjectId(session['user_id'])}, {"$set": {"password": generate_password_hash(new_password)}})
        flash('Password changed successfully! Please login again.', 'success')
        return redirect(url_for('logout'))

    return render_template('admin_reset_password.html')


# ----------------- Password reset email -----------------

def send_password_reset_email(user_email, reset_token):
    try:
        reset_link = url_for('reset_password', token=reset_token, _external=True)
        msg = Message(
            subject='Dairy Management - Password Reset Request',
            recipients=[user_email],
            html=f'''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
              <div style="background: linear-gradient(135deg, #2d5016 0%, #52b788 100%); padding: 20px; text-align: center; color: white; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0;">Dairy Management System</h1>
              </div>
              <div style="background: #fefae0; padding: 30px; border-radius: 0 0 8px 8px;">
                <p style="color: #333; font-size: 16px;">Hello,</p>
                <p style="color: #666; font-size: 14px; line-height: 1.6;">We received a request to reset your password. Click the button below to create a new password.</p>
                <div style="text-align: center; margin: 30px 0;">
                  <a href="{reset_link}" style="background: linear-gradient(135deg, #2d5016 0%, #52b788 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">Reset Password</a>
                </div>
                <p style="color: #666; font-size: 12px;">If you didn't request a password reset, ignore this email. The link above will expire in 1 hour.</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #999; font-size: 12px; text-align: center;">© 2025 Dairy Management System. All rights reserved.</p>
              </div>
            </div>
            '''
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = db.users.find_one({"email": email})

        if user:
            reset_token = secrets.token_urlsafe(32)
            db.users.update_one({"_id": user['_id']}, {"$set": {"reset_token": reset_token, "reset_token_expiry": datetime.now(timezone.utc) + timedelta(hours=1)}})

            if send_password_reset_email(email, reset_token):
                flash('Password reset link has been sent to your email!', 'success')
            else:
                reset_link = url_for('reset_password', token=reset_token, _external=True)
                flash('Email could not be sent. Here is your reset link (1 hour expiry):', 'warning')
                flash(f'Reset Link: {reset_link}', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email not found in our system', 'danger')

    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = db.users.find_one({"reset_token": token})
    if not user or user.get('reset_token_expiry') is None or user['reset_token_expiry'] < datetime.now(timezone.utc):
        flash('Invalid or expired reset link', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        if new_password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('reset_password', token=token))
        if len(new_password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('reset_password', token=token))

        db.users.update_one({"_id": user['_id']}, {"$set": {"password": generate_password_hash(new_password), "reset_token": None, "reset_token_expiry": None}})
        flash('Password reset successfully! Please login with your new password.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')


# ----------------- Error handlers -----------------

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


# ----------------- Run app -----------------

if __name__ == '__main__':
    debug = os.environ.get('ENV') != 'production'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug, host='0.0.0.0', port=port)
