# GitHub Authentication Configuration

This guide explains how to set up GitHub OAuth and GitHub App authentication for AlgeLab, including the creation of applications, configuration of callback URLs, and environment variables setup.

## Table of Contents
- [Prerequisites](#prerequisites)
- [GitHub OAuth App Setup](#github-oauth-app-setup)
- [GitHub App Setup](#github-app-setup)
- [Environment Variables](#environment-variables)
- [Callback URLs](#callback-urls)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

## Prerequisites

- GitHub account with administrative access
- Access to your deployment domain/URLs
- Access to your application's server configuration

## GitHub OAuth App Setup

1. Go to GitHub Developer Settings:
   - Navigate to your GitHub account
   - Go to Settings > Developer settings > OAuth Apps
   - Click "New OAuth App"

2. Fill in the application details:
   ```
   Application name: AlgeLab (Development/Production)
   Homepage URL: http://localhost:5173 (Development)
                https://your-domain.com (Production)
   Authorization callback URL: http://localhost:8000/api/auth/github/callback (Development)
                             https://your-domain.com/api/auth/github/callback (Production)
   ```

3. After creation, you'll receive:
   - Client ID
   - Client Secret (Generate a new client secret)

## GitHub App Setup

1. Go to GitHub Developer Settings:
   - Navigate to Settings > Developer settings > GitHub Apps
   - Click "New GitHub App"

2. Configure the application:
   ```
   GitHub App name: AlgeLab-SSO
   Homepage URL: Your application URL
   Webhook URL: Your webhook URL (optional)
   ```

3. Set permissions:
   - User permissions:
     - Email addresses: Read-only
     - Profile information: Read-only

4. Generate and download private key:
   - Click "Generate a private key"
   - Save as `algelab-sso.2024-10-02.private-key.pem`
   - Note the App ID

## Environment Variables

Add these variables to your `.env.development` or `.env.production`:

```env
# GitHub OAuth Settings
GITHUB_APP_ID=your_github_app_id
GITHUB_CLIENT_ID=your_oauth_client_id
GITHUB_CLIENT_SECRET=your_oauth_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/github/callback
GITHUB_PRIVATE_KEY_PATH=./algelab-sso.2024-10-02.private-key.pem

# For production, use your domain:
# GITHUB_REDIRECT_URI=https://your-domain.com/api/auth/github/callback
```

## Callback URLs

### Development URLs
```
Frontend: http://localhost:5173
Backend API: http://localhost:8000
Callback URL: http://localhost:8000/api/auth/github/callback
```

### Production URLs
```
Frontend: https://your-domain.com
Backend API: https://api.your-domain.com
Callback URL: https://your-domain.com/api/auth/github/callback
```

## Testing

1. Test OAuth Flow:
   - Start your application
   - Click "Login with GitHub"
   - Authorize the application
   - Verify redirect to your application
   - Check user profile data

2. Verify Scope Access:
   - Ensure email access
   - Verify profile information retrieval
   - Test token generation and validation

## Troubleshooting

Common issues and solutions:

1. **Invalid callback URL**
   - Verify exact match in GitHub settings
   - Check for trailing slashes
   - Ensure protocol (http/https) matches

2. **Authentication fails**
   - Verify client ID and secret
   - Check environment variables
   - Validate private key permissions

3. **Missing user data**
   - Verify OAuth scopes
   - Check API permissions
   - Validate token access

## Security Best Practices

1. Keep credentials secure:
   - Never commit .env files
   - Secure private key storage
   - Use environment variables

2. Production settings:
   - Enable HTTPS
   - Set secure cookie flags
   - Implement rate limiting

3. Access control:
   - Limit OAuth scopes
   - Regular key rotation
   - Monitor access logs

## Getting Official Credentials

For official AlgeLab GitHub credentials and configurations:

### Discord Support
Join our Discord server:
```
https://discord.gg/Q8F6xm7U
```

### Email Contact
Contact the main contributor:
```
mauro.bonillaol@anahuac.mx
```

## File Locations

Ensure these files are in their correct locations:

```
project_root/
├── .env.development
├── .env.production
└── algelab-sso.2024-10-02.private-key.pem
```

Remember to:
- Set correct file permissions (600) for the private key
- Keep the private key secure
- Never commit sensitive files to version control

## Additional Resources

- [GitHub OAuth documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [GitHub Apps documentation](https://docs.github.com/en/developers/apps/getting-started-with-apps)
- Project documentation in the [docs](../docs) directory