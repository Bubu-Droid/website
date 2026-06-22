import os
from pathlib import Path

from dotenv import load_dotenv

_ = load_dotenv()

assert "DEBUG" in os.environ, "DEBUG missing!"
assert "SECRET_KEY" in os.environ, "SECRET_KEY missing!"
assert "EMAIL_HOST_USER" in os.environ, "EMAIL_HOST_USER missing!"
assert "EMAIL_HOST_PASSWORD" in os.environ, "EMAIL_HOST_PASSWORD missing!"

DEBUG = os.getenv("DEBUG") == "TRUE"
SECRET_KEY = os.getenv("SECRET_KEY")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = [
    "www.bubudroid.me",
    # ".vercel.app",
    "127.0.0.1",
    ".localhost",
]

ADMINS = [("BubuDroid", "fufudadw@gmail.com")]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER

if not DEBUG:
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

INSTALLED_APPS = [
    "postapp.apps.PostAppConfig",
    "main.apps.MainConfig",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "website.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": (["console"] if DEBUG else []),
            "level": "WARNING",
            "propagate": True,
        },
        "django.request": {
            "handlers": (["mail_admins"] if not DEBUG else ["console"]),
            "level": "ERROR",
            "propagate": False,
        },
    },
}
