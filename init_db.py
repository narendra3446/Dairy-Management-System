"""
Initialize the database with sample data for testing
Run this after running: python app.py
"""

from app import app, db, User, Product
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
        else:
            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@dairy.com',
                password=generate_password_hash('N@3re4nd4ra6'),
                phone='9999999999',
                address='Dairy Admin Office',
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
        
        # Add sample products
        products = [
            Product(
                name='Fresh Milk',
                description='100% Pure Cow Milk',
                price=60,
                stock=100,
                unit='Liter'
            ),
            Product(
                name='Yogurt',
                description='Creamy Homemade Yogurt',
                price=80,
                stock=50,
                unit='kg'
            ),
            Product(
                name='Buttermilk',
                description='Refreshing Fresh Buttermilk',
                price=40,
                stock=75,
                unit='Liter'
            ),
            Product(
                name='Paneer',
                description='Soft and Fresh Paneer',
                price=250,
                stock=30,
                unit='kg'
            ),
            Product(
                name='Butter',
                description='Pure Cultured Butter',
                price=300,
                stock=25,
                unit='kg'
            ),
            Product(
                name='Cheese',
                description='Mild Cheese',
                price=400,
                stock=20,
                unit='kg'
            ),
            Product(
                name='Milk Cream',
                description='Rich and Thick Cream',
                price=120,
                stock=40,
                unit='kg'
            ),
            Product(
                name='Ghee',
                description='Pure Clarified Butter',
                price=600,
                stock=15,
                unit='kg'
            ),
        ]
        
        # Check if products already exist
        existing_products = Product.query.count()
        if existing_products > 0:
            print(f"{existing_products} products already exist in database!")
        else:
            for product in products:
                db.session.add(product)
            db.session.commit()
            print(f"{len(products)} sample products added successfully!")
        
        print("\nDatabase initialization complete!")
        print("\nYou can now login with:")
        print("URL: http://localhost:5000")
        print("Admin - Username: admin, Password: admin123")

if __name__ == '__main__':
    init_database()
