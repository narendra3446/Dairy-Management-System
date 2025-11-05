# Dairy Management System - Complete Setup Guide

## Quick Start (5 Minutes)

### 1. Install Python
- Download Python 3.8+ from python.org
- Make sure to check "Add Python to PATH" during installation

### 2. Setup Project Folder
\`\`\`bash
# Navigate to your desired folder
cd /path/to/your/folder

# Extract the zip file if you have it
unzip dairy-management.zip
cd dairy-management-system
\`\`\`

### 3. Create Virtual Environment
**On Windows:**
\`\`\`bash
python -m venv venv
venv\Scripts\activate
\`\`\`

**On macOS/Linux:**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 4. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 5. Initialize Database
\`\`\`bash
python init_db.py
\`\`\`

### 6. Run Application
\`\`\`bash
python app.py
\`\`\`

Open your browser and go to: **http://localhost:5000**

## Login Credentials

### Admin Account (After running init_db.py)
- **Username**: admin
- **Password**: admin123

### Create New User Account
- Click on "Register here" link on login page
- Fill in all details
- Click Register
- Login with your new credentials

## First Steps

### Step 1: Login as Admin
1. Go to http://localhost:5000
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click Login

### Step 2: Explore Admin Dashboard
You'll see:
- Total Products
- Total Users
- Total Orders
- Total Revenue
- Recent Orders

### Step 3: Manage Products
1. Click on "Products" in navigation
2. View all available products
3. Click "Add New Product" to create new
4. Click "Edit" to modify existing
5. Click "Delete" to remove

### Step 4: Add Sample Products
1. Click "Products" → "Add New Product"
2. Fill in details:
   - **Product Name**: Fresh Milk
   - **Description**: Pure Cow Milk
   - **Price**: 60
   - **Stock**: 50
   - **Unit**: Liter
3. Click "Add Product"

### Step 5: View Orders
1. Click on "Orders" to see all customer orders
2. Change order status from dropdown
3. View order items by clicking "View Details"

### Step 6: View User Purchases
1. Click on "Users" to see all registered users
2. See total orders per user
3. View user contact information

### Step 7: Check Reports
1. Click on "Reports" in navigation
2. See daily sales data
3. Check inventory levels
4. Identify low-stock items

## User Account Usage

### Register as Regular User
1. Go to http://localhost:5000
2. Click "Register here"
3. Fill registration form:
   - Username
   - Email
   - Password
   - Phone Number
   - Address
4. Click "Register"
5. Login with credentials

### Browse and Order Products
1. After login, you'll see all available products
2. Enter quantity for each product
3. Click "Add to Cart"
4. Review cart items
5. Click "Place Order"
6. You'll get order receipt
7. Can view order history in "My Orders"

### View Receipt
1. Go to "My Orders"
2. Click "View Receipt" for any order
3. Can print receipt for records
4. Shows delivery date and status

## Troubleshooting

### Problem: "Port 5000 already in use"
**Solution:**
\`\`\`bash
# Use a different port
python app.py --port 5001
# Then access at http://localhost:5001
\`\`\`

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
\`\`\`bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
\`\`\`

### Problem: "No such table: users"
**Solution:**
\`\`\`bash
# Run initialization script
python init_db.py
\`\`\`

### Problem: "Admin not working"
**Solution:**
1. Delete dairy_management.db file
2. Run: \`python init_db.py\`
3. Try again

### Problem: Can't access the website
**Solution:**
1. Check if app.py is running (should show "Running on http://localhost:5000")
2. Open browser and type: http://localhost:5000
3. If still not working, try: http://127.0.0.1:5000

## File Explanations

| File | Purpose |
|------|---------|
| app.py | Main application and database models |
| routes.py | All URL routes and logic |
| config.py | Configuration settings |
| init_db.py | Database initialization script |
| requirements.txt | Python packages needed |
| templates/ | HTML files for web pages |
| dairy_management.db | SQLite database (created automatically) |

## Database Structure

### Users
Stores customer and admin information

### Products
Stores all dairy products available for sale

### Orders
Tracks all customer orders with status

### OrderItems
Details of products in each order

## Features Summary

### User Features
- User registration and login
- Browse available dairy products
- Add products to shopping cart
- Place orders
- View order history
- Download order receipts
- See order status and delivery date

### Admin Features
- View dashboard with statistics
- Add, edit, delete products
- Manage stock inventory
- View all customer orders
- Update order status
- View customer list
- Generate sales reports
- Monitor daily revenue
- Check low-stock items

## Tips

1. Always activate virtual environment before running
2. Keep requirements.txt updated
3. Regular database backups recommended
4. Change admin password in production
5. Use environment variables for sensitive data

## Advanced Setup (Optional)

### Use with PostgreSQL (Production)
1. Install PostgreSQL
2. Create database
3. Update SQLALCHEMY_DATABASE_URI in config.py
4. Run: \`python init_db.py\`

### Deploy to Heroku
1. Create Heroku account
2. Install Heroku CLI
3. Create Procfile with: \`web: python app.py\`
4. Deploy using: \`git push heroku main\`

## Getting Help

If you face any issues:
1. Check this guide first
2. Review the README.md file
3. Check error messages in terminal
4. Ensure all files are in correct folders
5. Try running init_db.py to reset database

---

**Happy Dairy Management!**
