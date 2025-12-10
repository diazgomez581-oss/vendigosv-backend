# settings.py

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# 1. SECRET KEY & DEBUG
# ============================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-t+(u8j09jxbikpfifxl4#=v*^+$_$e=prnzf-ov##omt1yqz8u')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'


# ============================================================
# 2. ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,**vendigosv-backend.onrender.com**,vendigosv.com,api.vendigosv.com'
).split(',')


# ============================================================
# 3. SECURITY FOR DEVELOPMENT
# ============================================================

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'


# ============================================================
# 4. INSTALLED APPS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'myapp',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
]


# ============================================================
# 5. REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'myapp.authentication.CustomHeaderAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}


# ============================================================
# 6. MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'api.urls'


# ============================================================
# 7. TEMPLATES
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ============================================================
# 8. WSGI
# ============================================================

WSGI_APPLICATION = 'api.wsgi.application'


# ============================================================
# 9. DATABASE CONFIG (FINAL & CORRECTA PARA RENDER)
# ============================================================

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgresql://admin_vendigo:admin@localhost:5432/vendigo_main"
        ),
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}


# ============================================================
# 10. PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================
# 11. MEDIA FILES
# ============================================================

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# ============================================================
# 12. LOCALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ============================================================
# 13. STATIC FILES
# ============================================================

STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# 14. CORS
# ============================================================

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-user-id',
]


# ============================================================
# 15. CSRF TRUSTED ORIGINS (FINAL)
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    'https://n009hzjf-8000.use.devtunnels.ms',
    'https://n009hzjf-5173.use.devtunnels.ms',
    'https://vendigosv-backend.onrender.com',
    'https://vendigosv.com',
    'https://api.vendigosv.com',
]
