# Deployment Guide - Dairy Management System

This guide covers deploying your Dairy Management System to various platforms for public access.

## Prerequisites

- Python 3.8+
- Git account
- GitHub repository created
- Deployment platform account (choose one below)

## Step 1: Prepare Your Code

### 1.1 Initialize Git Repository

\`\`\`bash
git init
git add .
git commit -m "Initial commit: Dairy Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dairy-management.git
git push -u origin main
\`\`\`

### 1.2 Create Environment Variables

Create a `.env` file (do not commit to GitHub):

\`\`\`
ENV=production
SECRET_KEY=your-very-secure-random-key-here
DATABASE_URL=sqlite:///dairy_management.db
PORT=5000
\`\`\`

Generate a strong SECRET_KEY:
\`\`\`python
import secrets
print(secrets.token_urlsafe(32))
\`\`\`

## Option 1: Deploy to Heroku (Easiest)

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Steps

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku**:
   \`\`\`bash
   heroku login
   \`\`\`

3. **Create Heroku App**:
   \`\`\`bash
   heroku create your-app-name
   \`\`\`

4. **Set Environment Variables**:
   \`\`\`bash
   heroku config:set SECRET_KEY="your-secure-key"
   heroku config:set ENV=production
   \`\`\`

5. **Deploy**:
   \`\`\`bash
   git push heroku main
   \`\`\`

6. **View Logs**:
   \`\`\`bash
   heroku logs --tail
   \`\`\`

7. **Open Your App**:
   \`\`\`bash
   heroku open
   \`\`\`

Your app will be accessible at: `https://your-app-name.herokuapp.com`

---

## Option 2: Deploy to Railway

### Prerequisites
- Railway account: https://railway.app
- GitHub connected to Railway

### Steps

1. **Go to Railway Dashboard**: https://railway.app/dashboard

2. **Create New Project** → Select "Deploy from GitHub"

3. **Select Your Repository** and authorize

4. **Add Variables** in Railway dashboard:
   - `SECRET_KEY`: Your secure key
   - `ENV`: `production`
   - `DATABASE_URL`: Defaults to SQLite

5. **Deploy** - Railway automatically deploys on every push to main

6. **Get Your Domain** - Railway provides a public URL automatically

---

## Option 3: Deploy to Render

### Prerequisites
- Render account: https://render.com
- GitHub connected to Render

### Steps

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **Create New Web Service** → Select "Public Git Repository"

3. **Connect Your GitHub Repo**

4. **Configure Settings**:
   - **Name**: dairy-management
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Instance Type**: Free (or paid for better performance)

5. **Add Environment Variables**:
   - `SECRET_KEY`: Your secure key
   - `ENV`: `production`

6. **Deploy** - Render automatically deploys on push

Your app will be accessible at: `https://your-app-name.onrender.com`

---

## Option 4: Deploy to PythonAnywhere

### Prerequisites
- PythonAnywhere account: https://www.pythonanywhere.com
- Free tier available

### Steps

1. **Upload Files**:
   - Use Web interface or Git clone
   - Upload all project files

2. **Create Web App**:
   - Web → Add a new web app
   - Choose Python 3.10
   - Choose Flask

3. **Configure WSGI File**:
   - Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Point to your `wsgi.py`

4. **Set Up Virtual Environment**:
   \`\`\`bash
   mkvirtualenv --python=/usr/bin/python3.10 dairy-env
   pip install -r requirements.txt
   \`\`\`

5. **Configure Database**:
   - Database path must be writable
   - Use absolute paths in DATABASE_URL

6. **Reload** your web app from the dashboard

Your app will be accessible at: `https://yourusername.pythonanywhere.com`

---

## Option 5: Deploy to DigitalOcean App Platform

### Prerequisites
- DigitalOcean account: https://www.digitalocean.com
- GitHub connected

### Steps

1. **Create App**:
   - App Platform → Create App
   - Select your GitHub repository

2. **Configure**:
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn wsgi:app`

3. **Set Environment Variables**:
   - `SECRET_KEY`: Your secure key
   - `ENV`: `production`

4. **Deploy**

Your app will be on: `https://your-app-name-xxxxx.ondigitalocean.app`

---

## Production Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `ENV=production`
- [ ] Use HTTPS (enabled automatically on most platforms)
- [ ] Set strong admin password after deployment
- [ ] Enable `SESSION_COOKIE_SECURE=True` in production
- [ ] Regularly backup your database
- [ ] Monitor error logs
- [ ] Keep dependencies updated

## Database Migration for Production

For large deployments, consider using PostgreSQL:

1. **Create PostgreSQL Database** (on your hosting provider)

2. **Update DATABASE_URL**:
   \`\`\`
   DATABASE_URL=postgresql://user:password@host:5432/dairy_management
   \`\`\`

3. **Install PostgreSQL driver**:
   \`\`\`bash
   pip install psycopg2-binary
   \`\`\`

4. **Redeploy** your application

## Custom Domain

To use your own domain (e.g., dairy.example.com):

1. **Purchase Domain** from registrar (GoDaddy, Namecheap, etc.)

2. **Point DNS to Your Hosting**:
   - Heroku: Create CNAME record
   - Railway: Add custom domain in settings
   - Render: Add custom domain in settings

3. **SSL Certificate** (auto-provisioned on most platforms)

## Monitoring & Maintenance

- Check logs regularly: `heroku logs --tail`
- Monitor uptime with StatusCake or Uptime Robot
- Set up error alerts
- Regular backups of database
- Update dependencies monthly

## Troubleshooting

### App won't start
- Check `ENV` and `SECRET_KEY` are set
- Review deployment logs
- Ensure `requirements.txt` is up-to-date

### Database errors
- Verify `DATABASE_URL` is correct
- Check database file permissions
- Migrate to PostgreSQL for scale

### 502/503 errors
- Check available memory on deployment platform
- Review error logs
- Restart application

## Support & Resources

- Heroku Docs: https://devcenter.heroku.com/
- Railway Docs: https://docs.railway.app/
- Render Docs: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com/
