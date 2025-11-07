"""
Initialize the MongoDB database with sample data for testing.
Run this after starting your Flask app (python app.py)
"""

from werkzeug.security import generate_password_hash
from app import db

def init_database():
    users = db.users
    products = db.products

    # Check if admin already exists
    if users.find_one({"username": "admin"}):
        print("✅ Admin user already exists!")
    else:
        admin_user = {
            "username": "admin",
            "email": "admin@dairy.com",
            "password": generate_password_hash("N@3re4nd4ra6"),
            "phone": "9999999999",
            "address": "Dairy Admin Office",
            "is_admin": True
        }
        users.insert_one(admin_user)
        print("👤 Admin user created successfully!")

    # Sample products
    sample_products = [
        {"name": "Fresh Milk", "description": "100% Pure Cow Milk", "price": 60, "stock": 100, "unit": "Liter"},
        {"name": "Yogurt", "description": "Creamy Homemade Yogurt", "price": 80, "stock": 50, "unit": "kg"},
        {"name": "Buttermilk", "description": "Refreshing Fresh Buttermilk", "price": 40, "stock": 75, "unit": "Liter"},
        {"name": "Paneer", "description": "Soft and Fresh Paneer", "price": 250, "stock": 30, "unit": "kg"},
        {"name": "Butter", "description": "Pure Cultured Butter", "price": 300, "stock": 25, "unit": "kg"},
        {"name": "Cheese", "description": "Mild Cheese", "price": 400, "stock": 20, "unit": "kg"},
        {"name": "Milk Cream", "description": "Rich and Thick Cream", "price": 120, "stock": 40, "unit": "kg"},
        {"name": "Ghee", "description": "Pure Clarified Butter", "price": 600, "stock": 15, "unit": "kg"},
    ]

    existing_products = products.count_documents({})
    if existing_products > 0:
        print(f"📦 {existing_products} products already exist!")
    else:
        products.insert_many(sample_products)
        print(f"🧀 {len(sample_products)} sample products added successfully!")

    print("\n✅ Database initialization complete!")
    print("You can now login with:")
    print("👉 Username: admin")
    print("👉 Password: admin123")

if __name__ == "__main__":
    init_database()
