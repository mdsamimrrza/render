# Render Deployment Guide for Django EdTech Project

## Quick Deploy Steps

### 1. Render Web Service Configuration

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

**OR use the build script:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn edtech_project.wsgi:application
```

### 2. Required Environment Variables

Add these in Render Dashboard → Environment:

```
PYTHON_VERSION=3.11.0
DEBUG=False
SECRET_KEY=<generate-new-secret-key>
ALLOWED_HOSTS=.onrender.com
```

### 3. Generate SECRET_KEY

Run locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Database Setup (Optional but Recommended)

**For PostgreSQL:**
1. Create PostgreSQL database in Render
2. Copy the `DATABASE_URL` 
3. Add it as environment variable in your web service

**For SQLite (Not Recommended for Production):**
- Current settings.py already supports SQLite fallback
- No additional configuration needed

### 5. Static Files

✅ Already configured with WhiteNoise
- STATIC_URL = '/static/'
- STATIC_ROOT = staticfiles/
- WhiteNoise middleware added

### 6. Deploy

1. Push code to GitHub: ✅ Already done
2. Create web service on Render
3. Render will auto-deploy from main branch
4. Visit your-app.onrender.com

## Post-Deployment

### Create Superuser

After first deploy, create admin user:
1. Go to Render Dashboard
2. Open Shell for your web service
3. Run:
```bash
python manage.py createsuperuser
```

### Check Logs

Monitor deployment in Render Dashboard → Logs

## Troubleshooting

**Static files not loading?**
- Verify STATIC_ROOT and collectstatic ran
- Check WhiteNoise middleware order

**Database errors?**
- Verify DATABASE_URL is set
- Check migrations ran successfully

**502 Bad Gateway?**
- Check Start Command uses correct WSGI path
- Verify gunicorn is in requirements.txt
