import os
from pathlib import Path
from datetime import timedelta
import environ
import psycopg2
from psycopg2 import OperationalError
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--ii!=x!r*thwn+^g%@3o(d#c@@g@w6uy507hbn&55$901^v=@m"
# SHIPBUBBLE_API_KEY = env('SHIPBUBBLE_API_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SITE_ID = 1

ALLOWED_HOSTS = [
    # Add allowed hostnames or IP addresses here
     'godhouse.org',
     'www.godhouse.org',
     'https://godhouse.org',
     'https://www.godhouse.org',
     'mail.godhouse.org',
     'localhost:8000',
     'localhost',
]

# Email configuration for Gmail SMTP
# SECURITY WARNING: Consider using environment variables for sensitive information
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'missionsgodhouse@gmail.com'
EMAIL_HOST_PASSWORD = 'qmpo qyzq iyvy dubc'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Application definition
# This list includes built-in Django apps, custom project apps, and third-party apps
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom project apps
    'sermons',
    'communnity',
    'contact',
    'core',
    'events',
    'giving',
    'praiseReport',
    'store',
    'WholeWordConference',
    'rezonance',
    'runningWithTheVisionConference',
    'ministrySchool',
    'WholeWordTv',
    'legal',
    
    # Third-party apps
    'tinymce',  # Rich text editor
    'django.contrib.humanize',  # Adds template filters for human-readable values
    "mptt",  # Modified Preorder Tree Traversal for hierarchical data
    'request',  # HTTP request logging
    'django_countries', # django countries package
    'phonenumber_field', # django phone number package
    'localflavor', # django states and province package
    'rest_framework',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'dj_rest_auth',
    # 'dj_rest_auth.registration',
    'channels',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'allauth.account.middleware.AccountMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CORS_ALLOW_CREDENTIALS = True


CORS_ALLOWED_ORIGINS = [
    "https://wholewordtv.godhouse.org",
    "http://localhost:8080",
    "https://www.wholewordtv.godhouse.org",
    "https://rvc.godhouse.org",
    "https://www.rvc.godhouse.org",
]

CSRF_TRUSTED_ORIGINS = [
    "https://wholewordtv.godhouse.org",
    "http://localhost:8080",
    "https://www.wholewordtv.godhouse.org",
    "https://rvc.godhouse.org",
    "https://www.rvc.godhouse.org",
]




ROOT_URLCONF = 'TheGodHouseCenter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.globalContext',
                'communnity.context_processors.churches',
                'legal.context_processors.legal',
            ],
        },
    },
]

WSGI_APPLICATION = 'TheGodHouseCenter.wsgi.application'


# Database configuration using environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CSRF_COOKIE_SECURE = True   # True in production
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"


#DATABASES = {
#    "default": dj_database_url.config(
#        default=env("SUPABASE_DB_URL"),
#        conn_max_age=600,
#        ssl_require=True
#    )
#}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS= [BASE_DIR / 'static']
STATIC_ROOT = 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'  # Add a leading slash for correct URL path
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]

# allauth settings
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'none'
# LOGIN_REDIRECT_URL = "/wholewordtv/"



# Social account providers with app credentials loaded from environment variables


# SOCIALACCOUNT_PROVIDERS = {
#     "google": {
#         "APP": {
#             "client_id": "547988421723-o7d92bh1vf7cqb670dkf823m8dspqv87.apps.googleusercontent.com",
#             "secret": "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",
#             "key": ""
#         },
#         "SCOPE": [
#             "profile",
#             "email",
#         ],
#         "AUTH_PARAMS": {
#             "access_type": "online",
#         },
#     }
# }

# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework.authentication.TokenAuthentication",
#     ],
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
# }

# REST_AUTH = {
#     'USE_JWT': False,
#     'JWT_AUTH_COOKIE': 'app-auth',
#     'JWT_AUTH_REFRESH_COOKIE': 'refreshtoken',
# }
