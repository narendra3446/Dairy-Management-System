"""
Initialize production database with sample data
Run this after deploying to production
"""
import os
from app_complete import app, db, User, Product
from werkzeug.security import generate_password_hash

def init_production_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@dairymanagement.com',
                password=generate_password_hash('ChangeMe123!'),
                phone='9999999999',
                address='Admin Address',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created. Username: admin, Password: ChangeMe123!")
            print("IMPORTANT: Change the admin password immediately!")
        
        # Add sample products
        sample_products = [
            {'name': 'Milk (1L)', 'description': 'Fresh cow milk', 'price': 50, 'stock': 100, 'unit': 'Liter'},
            {'name': 'Yogurt (500ml)', 'description': 'Natural yogurt', 'price': 40, 'stock': 50, 'unit': 'ml'},
            {'name': 'Butter (200g)', 'description': 'Pure butter', 'price': 120, 'stock': 30, 'unit': 'g'},
            {'name': 'Paneer (250g)', 'description': 'Fresh paneer cheese', 'price': 80, 'stock': 40, 'unit': 'g'},
            {'name': 'Buttermilk (1L)', 'description': 'Traditional buttermilk', 'price': 30, 'stock': 60, 'unit': 'Liter'},
        ]
        
        for product_data in sample_products:
            existing = Product.query.filter_by(name=product_data['name']).first()
            if not existing:
                product = Product(**product_data)
                db.session.add(product)
                print(f"Added product: {product_data['name']}")
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_production_db()
