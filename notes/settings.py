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
CSRF_TRUSTED_ORIGINS = [] # Initialize as an empty list

# Get the domain from RAILWAY_PUBLIC_DOMAIN if it's set
RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if RAILWAY_PUBLIC_DOMAIN:
    # RAILWAY_PUBLIC_DOMAIN might be just the hostname or a full URL.
    # If it's a full URL (e.g., https://domain.com), parse it.
    # If it's just a hostname (e.g., domain.com), use it directly.
    if '://' in RAILWAY_PUBLIC_DOMAIN: # Simple check if it looks like a full URL
        parsed_url = urlparse(RAILWAY_PUBLIC_DOMAIN)
        if parsed_url.hostname:
            ALLOWED_HOSTS.append(parsed_url.hostname)
            # Add to CSRF_TRUSTED_ORIGINS with the scheme
            CSRF_TRUSTED_ORIGINS.append(f"{parsed_url.scheme}://{parsed_url.hostname}")
    else: # Assume it's already a hostname
        ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
        # Add to CSRF_TRUSTED_ORIGINS, assuming https
        CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_PUBLIC_DOMAIN}")

# For local development when DEBUG is True
if DEBUG:
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')

# If ALLOWED_HOSTS is still empty in production (DEBUG=False),
# it means RAILWAY_PUBLIC_DOMAIN was not set or was invalid.
# Django will raise a DisallowedHost error, which is good for security.
# You could add a more explicit error here if you want:
# if not DEBUG and not ALLOWED_HOSTS and not CSRF_TRUSTED_ORIGINS: # Check CSRF_TRUSTED_ORIGINS too
#     from django.core.exceptions import ImproperlyConfigured
#     raise ImproperlyConfigured(
#         "ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS are not set. "
#         "Ensure the RAILWAY_PUBLIC_DOMAIN environment variable is correctly set in your Railway service."
#     )


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
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL='login'

