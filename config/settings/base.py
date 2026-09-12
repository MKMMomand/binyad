from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _


# =============================================================================
# BASE DIRECTORY & ENVIRONMENT
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")


# =============================================================================
# SECURITY
# =============================================================================

SECRET_KEY = env(
    "SECRET_KEY",
    default="dev-insecure-key-change-me",
)

DEBUG = env.bool(
    "DEBUG",
    default=False,
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
    ],
)


# =============================================================================
# APPLICATIONS
# =============================================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",

    # Local applications
    "apps.core",
    "apps.services",
    "apps.products",
    "apps.portfolio",
    "apps.blog",
    "apps.contact",
    "apps.pages",
]


# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # Binyad custom middleware
    "apps.core.middleware.URLPrefixLanguageMiddleware",

    # Django
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =============================================================================
# URL / APPLICATION CONFIGURATION
# =============================================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]


# =============================================================================
# DATABASE
# =============================================================================

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}


# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = "fa"

TIME_ZONE = "Asia/Kabul"

USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("fa", _("Dari / Persian")),
    ("ps", _("Pashto")),
    ("en", _("English")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# =============================================================================
# STATIC FILES
# =============================================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# WhiteNoise production storage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# =============================================================================
# MEDIA / UPLOADS
# =============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB

DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE

FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE


# =============================================================================
# EMAIL
# =============================================================================

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = env(
    "EMAIL_HOST",
    default="",
)

EMAIL_PORT = env.int(
    "EMAIL_PORT",
    default=587,
)

EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
    default="",
)

EMAIL_HOST_PASSWORD = env(
    "EMAIL_HOST_PASSWORD",
    default="",
)

EMAIL_USE_TLS = env.bool(
    "EMAIL_USE_TLS",
    default=True,
)

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="noreply@binyad.af",
)

CONTACT_NOTIFICATION_EMAIL = env(
    "CONTACT_NOTIFICATION_EMAIL",
    default="",
)


# =============================================================================
# WHATSAPP
# =============================================================================

WHATSAPP_NUMBER = env(
    "WHATSAPP_NUMBER",
    default="",
)


# =============================================================================
# SECURITY DEFAULTS
# =============================================================================

CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = "DENY"

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = "same-origin"


# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"