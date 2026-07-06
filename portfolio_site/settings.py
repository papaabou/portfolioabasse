from pathlib import Path
import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "development")

if ENVIRONMENT == "development":
    from dotenv import load_dotenv
    load_dotenv()

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-local-dev-key-123456789")

IS_PRODUCTION = ENVIRONMENT == "production"

DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = (
    os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
)

INTERNAL_IPS = ["127.0.0.1",]

# Debug toolbar is a dev-only tool; keep it out of the way when reviewing the
# site visually (it never renders in production regardless, since DEBUG=False there).
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: False,
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "core",
    "projects",
    "contact",
    "client",
    "services",
    "blog",
    "testimonials",
    "dashboard",
    "about_me",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_settings",
            ],
        },
    }
]

WSGI_APPLICATION = "portfolio_site.wsgi.app"

if IS_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

if IS_PRODUCTION:
    # Render's filesystem is ephemeral and the "logs/" dir isn't guaranteed to
    # exist, so log to the console only — Render captures stdout/stderr itself.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {'format': '[{levelname}] {message}', 'style': '{'},
        },
        'handlers': {
            'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
        },
        'loggers': {
            'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': True},
            'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
        },
    }
else:
    os.makedirs(BASE_DIR / 'logs', exist_ok=True)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '[{levelname}] {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs/django.log',
                'formatter': 'verbose',
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs/django_errors.log',
                'formatter': 'verbose',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file', 'error_file', 'console'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['error_file'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = (
    'django.core.mail.backends.smtp.EmailBackend'
    if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
    else 'django.core.mail.backends.console.EmailBackend'
)
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.environ.get("RESEND_FROM_EMAIL")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or RESEND_FROM_EMAIL or "no-reply@abasseniang.fr"
