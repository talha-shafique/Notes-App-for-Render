import os
import dj_database_url # Add this import
from pathlib import Path
from urllib.parse import urlparse # Add this for parsing Railway URL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Load SECRET_KEY from an environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Load DEBUG status from an environment variable, default to False
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = []
# For Railway, they provide a domain like your-service-name.up.railway.app
# You can get this from your Railway dashboard once deployed, or Railway might set an env var.
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL') # Railway often sets this
if RAILWAY_STATIC_URL:
    # RAILWAY_STATIC_URL might be the full URL (e.g., https://...). We need the hostname.
    parsed_url = urlparse(RAILWAY_STATIC_URL)
    if parsed_url.hostname:
        ALLOWED_HOSTS.append(parsed_url.hostname)

# It's a good idea to also add your specific service domain if you know it,
# e.g., 'my-django-notes-app.up.railway.app' (replace with your actual Railway service domain)
# You can find this on your Railway project's settings page after the first deploy attempt.
# Example:
# MY_RAILWAY_APP_DOMAIN = os.environ.get('MY_RAILWAY_APP_DOMAIN') # If you set this custom env var
# if MY_RAILWAY_APP_DOMAIN:
#     ALLOWED_HOSTS.append(MY_RAILWAY_APP_DOMAIN)

# For local development when DEBUG is True
if DEBUG:
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')

# If ALLOWED_HOSTS is empty after the above, and you are in production (DEBUG=False),
# Django will raise an error. Ensure at least one production domain is added.
# As a fallback, you might need to manually add your Railway domain if the env var isn't picked up initially:
# if not DEBUG and not ALLOWED_HOSTS:
#     # Replace 'your-app-name.up.railway.app' with your actual Railway domain
#     ALLOWED_HOSTS.append('your-app-name.up.railway.app')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Add this for development if you want to test whitenoise
    'django.contrib.staticfiles',
    'noteapp', # Assuming your app is named 'noteapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add Whitenoise middleware HERE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notes.urls'

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

WSGI_APPLICATION = 'notes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Use dj-database-url to parse the DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}', # Fallback to SQLite for local dev
        conn_max_age=600,
        ssl_require=os.environ.get('DATABASE_SSL_REQUIRE', 'False').lower() == 'true' # For Railway PostgreSQL, SSL is often required
    )
}

# If you are using Render's free PostgreSQL tier, SSL might be required.
# Check Render's documentation. If so, you might need:
# if os.environ.get('DATABASE_URL'): # Only apply SSL if DATABASE_URL is set (i.e., in production)
#     DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
# This is where Django will collect all static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add Whitenoise storage. This will compress your static files and add unique names.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# If you have a project-level static directory (not inside an app)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles') # Or your preferred media root

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
