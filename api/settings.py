# settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. SEGURIDAD - SECRET_KEY y DEBUG
# Lee SECRET_KEY del entorno de Render.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-t+(u8j09jxbikpfifxl4#=v*^+$_$e=prnzf-ov##omt1yqz8u')

# Lee DJANGO_DEBUG del entorno de Render (debe ser 'False' en Render).
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# 2. ALLOWED_HOSTS (CORREGIDO)
# Lee DJANGO_ALLOWED_HOSTS del entorno de Render.
# Se añade **.onrender.com para aceptar el host de producción.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,n009hzjf-8000.use.devtunnels.ms,n009hzjf-5173.use.devtunnels.ms,*.onrender.com,**vendigosv.com**, **api.vendigosv.com**').split(',')

# ====================================================================
# CONFIGURACIONES DE SEGURIDAD PARA DESARROLLO (Mantenidas)
# ====================================================================
SECURE_SSL_REDIRECT = False 
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False 
 
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

        'myapp.authentication.CustomHeaderAuthentication',
        
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}
 
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
 
# 3. DATABASES (CORREGIDO)
# Usa las variables de entorno de Render, y asegura que los valores por defecto (fallbacks) 
# coincidan con lo que configuraste en Render para que la migración funcione.
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        # Fallback a vendigo_main para la migración
        'NAME': os.environ.get('DB_NAME', 'vendigo_main'), 
        # Fallback a admin_vendigo para la migración
        'USER': os.environ.get('DB_USER', 'admin_vendigo'), 
        'PASSWORD': os.environ.get('DB_PASSWORD', 'tu_contraseña_local'),
        # HOST usará 'vendigo-db' en Render
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

# 4. CSRF_TRUSTED_ORIGINS (CORREGIDO)
# Se añade la URL potencial de tu backend en Render para permitir peticiones POST.
CSRF_TRUSTED_ORIGINS = [
    'https://n009hzjf-8000.use.devtunnels.ms',
    'https://n009hzjf-5173.use.devtunnels.ms',
    'https://vendigosv-backend.onrender.com', # Tu dominio de Render
    'https://*.onrender.com', # Añadir el comodín por seguridad
    # Añade aquí la URL segura (HTTPS) de tu dominio
    'https://vendigosv.com', 
    'https://api.vendigosv.com',
]