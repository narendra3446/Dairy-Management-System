# Dairy Management System

A complete web-based dairy management application built with Flask and SQLite. This system helps dairy businesses manage products, track inventory, process customer orders, and generate reports.

## Features

### User Panel
- Browse available dairy products
- Add products to cart
- Place orders online
- View order history and status
- Download/print receipts
- User registration and authentication

### Admin Panel
- Add, edit, and delete products
- Manage inventory and stock levels
- View all customer orders and track status
- Monitor customer purchases and history
- Generate sales reports and analytics
- Track revenue and daily sales

### Supported Products
- Milk (Liters)
- Yogurt (kg, pieces)
- Buttermilk (Liters)
- Paneer (kg)
- Cheese (kg)
- Butter (kg)
- And more!

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
\`\`\`bash
# If you have it as a zip file, extract it
unzip dairy-management.zip
cd dairy-management-system

# OR clone from GitHub
git clone https://github.com/YOUR_USERNAME/dairy-management.git
cd dairy-management
\`\`\`

### Step 2: Create a Virtual Environment
\`\`\`bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

### Step 3: Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 4: Initialize Database
\`\`\`bash
python init_db.py
\`\`\`

### Step 5: Run the Application
\`\`\`bash
python app_complete.py
\`\`\`

The application will start on `http://localhost:5000`

### Default Credentials
- **Admin Username**: admin
- **Admin Password**: admin123
- **Test User**: user / user123

## First Time Setup

### Create Admin User
When you first run the application, follow these steps:

1. Register as a new user (any username)
2. Use this Python script to make the user an admin:

\`\`\`python
from app import app, db, User

with app.app_context():
    # Replace 'your_username' with the username you registered
    user = User.query.filter_by(username='your_username').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print(f"User {user.username} is now an admin!")
    else:
        print("User not found")
\`\`\`

Or run this command after registration:
\`\`\`bash
python -c "from app import app, db, User; app.app_context().push(); u=User.query.filter_by(username='admin').first(); u.is_admin=True if u else None; db.session.commit() if u else None; print('Admin created' if u else 'User not found')"
\`\`\`

### Add Sample Products
1. Login as admin
2. Go to Products > Add New Product
3. Add products like:
   - Milk (₹60/Liter)
   - Yogurt (₹80/kg)
   - Buttermilk (₹40/Liter)
   - Paneer (₹250/kg)

## Usage

### For Regular Users
1. Register with your details
2. Login to your account
3. Browse available dairy products
4. Select products and add to cart
5. Place order
6. View order receipt
7. Check order status in "My Orders"

### For Administrators
1. Login with admin credentials
2. Access admin dashboard for overview
3. **Manage Products**: Add, edit, delete products
4. **Manage Orders**: Update order status
5. **View Reports**: Monitor sales and inventory
6. **View Users**: See all registered customers

## Project Structure
\`\`\`
dairy-management/
│
├── app_complete.py          # Main Flask application (production-ready)
├── wsgi.py                  # WSGI entry point for production servers
├── init_db.py              # Database initialization script
├── init_db_production.py   # Production database setup
├── config_production.py    # Production configuration
├── requirements.txt        # Python dependencies
├── Procfile                # Heroku deployment configuration
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose for local development
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── user_dashboard.html
│   ├── user_orders.html
│   ├── receipt.html
│   ├── admin_dashboard.html
│   ├── admin_products.html
│   ├── admin_orders.html
│   ├── admin_users.html
│   ├── admin_reports.html
│   ├── add_product.html
│   ├── edit_product.html
│   └── error pages (404.html, 500.html)
│
├── .github/
│   ├── workflows/          # CI/CD workflows
│   │   ├── deploy.yml      # Auto-deployment
│   │   └── tests.yml       # Automated testing
│   ├── CONTRIBUTING.md     # Contributing guidelines
│   └── ISSUE_TEMPLATE/     # GitHub issue templates
│
├── Documentation Files
│   ├── README.md               # This file
│   ├── DEPLOYMENT_GUIDE.md     # Deployment instructions
│   ├── QUICK_DEPLOY.md         # 5-minute deploy guide
│   ├── GITHUB_SETUP.md         # GitHub setup guide
│   ├── PRODUCTION_CHECKLIST.md # Pre-deployment checklist
│   ├── SECURITY.md             # Security policy
│   └── LICENSE                 # MIT License
│
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── dairy_management.db     # SQLite database (created automatically)
\`\`\`

## Database Schema

### Users Table
- id, username, email, password, phone, address, is_admin, created_at

### Products Table
- id, name, description, price, stock, unit, created_at

### Orders Table
- id, user_id, total_amount, status, order_date, delivery_date

### OrderItems Table
- id, order_id, product_id, quantity, price, subtotal

## Important Notes

### Security
- Change the SECRET_KEY in app.py or config.py for production
- Use environment variables for sensitive data
- Hash passwords using werkzeug (already implemented)

### Database Backup
Regular SQLite database backups are recommended for production.

## Production Deployment

Your application is now production-ready and can be deployed to public servers!

### Quick Deployment Options

#### Option 1: Railway (Recommended - Fastest)
\`\`\`bash
# 1. Push to GitHub
git push origin main

# 2. Go to railway.app → Dashboard
# 3. New Project → Deploy from GitHub
# 4. Select dairy-management repository
# 5. Set environment variables and deploy!
\`\`\`
**Live URL**: `https://your-project.up.railway.app`

#### Option 2: Heroku
\`\`\`bash
heroku create dairy-app-yourname
heroku config:set SECRET_KEY="your-secure-key"
git push heroku main
heroku open
\`\`\`
**Live URL**: `https://dairy-app-yourname.herokuapp.com`

#### Option 3: Render
Go to render.com → New Web Service → Connect GitHub → Select dairy-management → Deploy

**Live URL**: `https://dairy-app-yourname.onrender.com`

#### Option 4: PythonAnywhere
Upload project to PythonAnywhere, configure WSGI, and access at your custom URL.

**Live URL**: `https://yourusername.pythonanywhere.com`

#### Option 5: Docker
\`\`\`bash
docker-compose up -d
\`\`\`
Access at `http://localhost:5000`

### Detailed Deployment Guide
See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for step-by-step instructions for each platform.

### Quick Deploy Checklist
See **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** for a 5-minute deployment guide.

## GitHub Repository

To push this project to GitHub:

\`\`\`bash
# Initialize Git
git init
git add .
git commit -m "Initial commit: Production-ready Dairy Management System"
git branch -M main

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/dairy-management.git
git push -u origin main
\`\`\`

See **[GITHUB_SETUP.md](GITHUB_SETUP.md)** for complete GitHub setup instructions.

### Features Included
- Automated tests on every push (GitHub Actions)
- Auto-deployment to Heroku on merge to main
- Issue templates for bug reports and features
- Contributing guidelines
- Security policy

## Environment Variables

For production deployment, create a `.env` file:

\`\`\`
ENV=production
SECRET_KEY=your-very-secure-random-key-here
DATABASE_URL=sqlite:///dairy_management.db
PORT=5000
\`\`\`

Generate a secure SECRET_KEY:
\`\`\`python
import secrets
print(secrets.token_urlsafe(32))
\`\`\`

**Never commit `.env` to GitHub!** It's included in `.gitignore`

## Security

### Production Security Checklist
- [ ] Set strong `SECRET_KEY` environment variable
- [ ] Set `ENV=production`
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Change admin password from default
- [ ] Use strong database passwords (if using PostgreSQL)
- [ ] Regularly update dependencies
- [ ] Enable security headers
- [ ] Set up error monitoring

See **[SECURITY.md](SECURITY.md)** for complete security guidelines.

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
\`\`\`bash
python app_complete.py --port 5001
# OR set environment variable
export PORT=5001
python app_complete.py
\`\`\`

### Database Issues
To reset the database:
\`\`\`bash
# Delete the dairy_management.db file
rm dairy_management.db  # Linux/Mac
del dairy_management.db  # Windows

# Restart the app (it will recreate the database)
python app_complete.py
\`\`\`

### Import Errors
Make sure all dependencies are installed:
\`\`\`bash
pip install -r requirements.txt --upgrade
\`\`\`

### Deployment Issues
- Check logs on your hosting platform
- Verify environment variables are set
- Ensure `SECRET_KEY` is configured
- See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for platform-specific issues

## Contributing

We welcome contributions! See **[.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)** for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support

- GitHub Issues: https://github.com/YOUR_USERNAME/dairy-management/issues
- Deployment Help: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Security Issues: See [SECURITY.md](SECURITY.md)

---

**Version**: 1.0 - Production Ready
**Last Updated**: November 2025
**Status**: Ready for Public Deployment
