# Deploying to Render

Render is a modern hosting platform that makes deployment simple. Follow these steps:

## Step 1: Create Render Account

1. Go to https://render.com
2. Click **"Sign up"**
3. Choose **"Sign up with GitHub"** (recommended)
4. Authorize Render to access your GitHub

## Step 2: Create New Web Service

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your **`dairy-management-app`** repository
5. Click **"Connect"**

## Step 3: Configure Service Settings

Fill in these fields:

- **Name**: `dairy-management-app`
- **Environment**: `Python 3`
- **Region**: Choose closest to your location
- **Branch**: `main`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`

## Step 4: Add Environment Variables

Click **"Environment"** and add these variables:

\`\`\`
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=sqlite:///dairy.db
\`\`\`

**Generate SECRET_KEY:**
\`\`\`bash
python -c "import secrets; print(secrets.token_hex(32))"
\`\`\`

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Build your app (watch the logs)
   - Deploy to production
   - Assign a public URL

3. Wait for deployment to complete (3-5 minutes)

## Step 6: Get Your Public URL

Once deployment succeeds:
- Your app is live at: `https://dairy-management-app.onrender.com`
- Render generates a unique subdomain

## Step 7: Initialize Database

1. In Render dashboard, go to **"Shell"** tab
2. Run:
   \`\`\`bash
   python init_db.py
   \`\`\`
3. This creates the database and sample data

## Step 8: Test Your App

1. Visit your Render URL
2. Create user account
3. Test admin login (admin / admin123)
4. **IMPORTANT**: Change admin password immediately

## Step 9: Change Admin Password

In Render Shell:
\`\`\`bash
python
\`\`\`

Then run:
\`\`\`python
from app_complete import db, User, app
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.set_password('YourNewSecurePassword123!')
        db.session.commit()
        print("✓ Admin password updated!")
\`\`\`

Press `Ctrl + D` to exit.

## Troubleshooting

### App shows blank page or error
- Check **"Logs"** tab in Render dashboard
- Click **"Redeploy"** if needed

### Database not initialized
- Go to Shell tab
- Run `python init_db.py` again

### Can't access admin panel
- Verify admin password was changed
- Check environment variables are set

## Auto-Deploy on GitHub Push

To automatically redeploy when you push to GitHub:

1. Make changes to your code
2. Push to `main` branch:
   \`\`\`bash
   git add .
   git commit -m "Your message"
   git push origin main
   \`\`\`
3. Render automatically redeploys (watch logs)

## Database Backups

SQLite databases on Render are ephemeral and may be lost. For important data:

1. Regularly download your `dairy.db` file
2. In Render Shell: 
   \`\`\`bash
   cat dairy.db > /tmp/backup.db
   \`\`\`
3. Download through dashboard

Or upgrade to PostgreSQL for persistent storage.

## Monitoring

- **Logs**: Check real-time logs in dashboard
- **Metrics**: Monitor CPU, memory, requests
- **Alerts**: Set up email alerts for errors

---

**Your app is now LIVE on Render!** 🚀
