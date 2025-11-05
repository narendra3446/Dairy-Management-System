# GitHub Repository Setup Guide

Follow these steps to set up your dairy management project on GitHub for production deployment.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `dairy-management`
3. Description: "A comprehensive web-based dairy management system"
4. Choose public (for public access)
5. Initialize with README (optional - we have one)
6. Click "Create repository"

## Step 2: Initialize Local Git

\`\`\`bash
cd dairy-management
git init
git add .
git commit -m "Initial commit: Dairy Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dairy-management.git
git push -u origin main
\`\`\`

## Step 3: Configure GitHub Secrets (for CI/CD)

If using automated deployments:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `HEROKU_API_KEY`: Get from Heroku account settings
   - `HEROKU_APP_NAME`: Your Heroku app name
   - `HEROKU_EMAIL`: Your Heroku email

## Step 4: Enable GitHub Pages (Optional)

For documentation:

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, folder: /docs
4. Save

## Step 5: Add Branch Protection Rules

1. Settings → Branches
2. Add rule for `main`:
   - Require a pull request before merging
   - Require status checks to pass before merging
   - Include administrators

## Step 6: Enable Issues & Discussions

1. Settings → General
2. Enable "Issues"
3. Enable "Discussions" (optional)

## Step 7: Add Collaborators (Optional)

1. Settings → Collaborators
2. Add team members
3. Set appropriate permissions

## Making Your First Release

\`\`\`bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
\`\`\`

Then go to GitHub → Releases and create release notes.

## File Structure for GitHub

Your repository should look like:

\`\`\`
dairy-management/
├── app_complete.py
├── wsgi.py
├── init_db.py
├── requirements.txt
├── config_production.py
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── README.md
├── LICENSE
├── SECURITY.md
├── DEPLOYMENT_GUIDE.md
├── GITHUB_SETUP.md
├── .gitignore
├── .env.example
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml
│   │   └── tests.yml
│   ├── CONTRIBUTING.md
│   └── ISSUE_TEMPLATE/
├── templates/
│   ├── base.html
│   ├── login.html
│   └── ...
└── instance/
    └── dairy_management.db (not committed)
\`\`\`

## Continuous Integration

GitHub Actions automatically:
- Tests code on every push/PR
- Runs security checks
- Deploys to Heroku on merge to main

View status: Actions tab in repository

## Getting Help

- GitHub Docs: https://docs.github.com
- GitHub Discussions: Enable in Settings
- Issues: Use for bug reports and feature requests
