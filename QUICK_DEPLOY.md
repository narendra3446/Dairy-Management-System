# Quick Deploy Guide - Choose Your Platform

## Fastest Option: Railway (5 minutes)

\`\`\`bash
# 1. Push to GitHub
git push origin main

# 2. Go to railway.app → Dashboard
# 3. New Project → Deploy from GitHub
# 4. Select your dairy-management repo
# 5. Add environment variables:
#    - SECRET_KEY: (generate one)
#    - ENV: production
# 6. Done! Check your live URL
\`\`\`

## Alternative: Heroku (7 minutes)

\`\`\`bash
# 1. Install Heroku CLI
# 2. Login: heroku login
# 3. Create app: heroku create dairy-app-yourname
# 4. Set secrets: 
heroku config:set SECRET_KEY="your-secure-key"
# 5. Deploy: git push heroku main
# 6. Open: heroku open
\`\`\`

## Alternative: Render (5 minutes)

\`\`\`bash
# 1. Go to render.com
# 2. New Web Service
# 3. Connect GitHub repo (dairy-management)
# 4. Build: pip install -r requirements.txt
# 5. Start: gunicorn wsgi:app
# 6. Add environment: SECRET_KEY, ENV=production
# 7. Deploy!
\`\`\`

## After Deployment

### Important: Change Admin Password

1. Login as `admin` / `admin123`
2. User Settings → Change Password
3. Set a strong password

### Test Everything

- [ ] User registration works
- [ ] Login works
- [ ] Can browse products
- [ ] Can place orders
- [ ] Admin panel accessible
- [ ] Can add products
- [ ] Can view receipts

### Share Your App

Your app is now live at:
- **Railway**: `https://your-project.up.railway.app`
- **Heroku**: `https://dairy-app-yourname.herokuapp.com`
- **Render**: `https://dairy-app-yourname.onrender.com`

Share this URL with users!

### Maintenance

- Monitor logs daily first week
- Update dependencies monthly
- Check for errors in logs
- Backup database regularly

## Need Help?

Check `DEPLOYMENT_GUIDE.md` for detailed instructions on each platform.
