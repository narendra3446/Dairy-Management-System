# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability, please email security@yourapp.com instead of using the issue tracker.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Security Best Practices

### Installation
- Always use virtual environments
- Verify package checksums
- Keep dependencies updated

### Configuration
- Never commit `.env` files
- Use strong SECRET_KEYs
- Rotate credentials regularly
- Use HTTPS in production

### Database
- Use parameterized queries (SQLAlchemy handles this)
- Regular backups
- Restrict database access
- Encrypt sensitive data

### User Management
- Enforce strong passwords
- Implement account lockout after failed attempts
- Audit admin actions
- Regular permission reviews

### Deployment
- Use environment variables for secrets
- Enable HTTPS/SSL
- Configure firewall rules
- Monitor access logs
- Keep servers patched

## Supported Versions

| Version | Status | Support Until |
|---------|--------|---------------|
| 1.0.x   | Active | 2026-12-31   |

## Known Issues

Currently no known security issues. Please report any findings responsibly.
