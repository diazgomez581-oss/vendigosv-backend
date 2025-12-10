# settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY desde variable de entorno (mejor práctica). Mantener valor por defecto para desarrollo.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-t+(u8j09jxbikpfifxl4#=v*^+$_$e=prnzf-ov##omt1yqz8u')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Permitir hosts comunes y el túnel público usado en devtunnels
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,n009hzjf-8000.use.devtunnels.ms,n009hzjf-5173.use.devtunnels.ms').split(',')

# ====================================================================
# ✅ CORRECCIONES PARA DESARROLLO (HTTP)
# Estas configuraciones resuelven el problema de las cookies 
# bloqueadas en navegadores que no son Brave (Chrome, Firefox, Edge).
# ====================================================================
SECURE_SSL_REDIRECT = False 
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False 

# Usa 'Lax' para asegurar que las cookies se envíen en peticiones 
# simples y evitar bloqueos en localhost.
SESSION_COOKIE_SAMESITE = 'Lax' 
CSRF_COOKIE_SAMESITE = 'Lax' 
# ====================================================================


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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Custom header authentication reads X-User-Id and maps to a Django user (implemented in myapp/authentication.py)
        'myapp.authentication.CustomHeaderAuthentication',
       # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# settings.py
MIDDLEWARE = [
    # 1. CORS DEBE IR LO MÁS ARRIBA POSIBLE
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 2. CSRF DEBE IR DESPUÉS DE LA SESIÓN Y SECURITY
    #'django.middleware.csrf.CsrfViewMiddleware', 
    # ... el resto
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'
 
 
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DB_NAME', 'vendigo'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'admin'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    },
}
 
 
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
  
STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOW_CREDENTIALS = True

# Allow common headers including our custom X-User-Id header used by the frontend
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

# If the frontend uses the public tunnel URL and sends cookies, add it here
CSRF_TRUSTED_ORIGINS = [
    'https://n009hzjf-8000.use.devtunnels.ms',
    'https://n009hzjf-5173.use.devtunnels.ms',
]