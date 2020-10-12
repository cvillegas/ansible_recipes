"""
Django settings for medicos voluntarios project.
"""
from pathlib import Path

from django.conf.global_settings import LANGUAGES
from django.utils.translation import ugettext_lazy as _

import environ

# Project settings
ROOT_DIR = Path(__file__).parents[2]

APPS_DIR = ROOT_DIR / "apps"

env = environ.Env()

# OS environment variables take precedence over variables from .env
env.read_env(str(ROOT_DIR / ".env"))

DEBUG = env.bool("DEBUG", False)

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_countries",
    "phonenumber_field",
    "rest_framework",
]

LOCAL_APPS = [
    "apps.common",
    "apps.consultas",
    "apps.especialidades",
    "apps.medicos",
    "apps.minsa",
    "apps.pacientes",
    "apps.persona",
    "apps.terms",
    "apps.permisos",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.InitMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader",],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}

DATABASES["default"]["ATOMIC_REQUESTS"] = True

DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

SPATIALITE_LIBRARY_PATH = env.str("SPATIALITE_LIBRARY_PATH", "")

# Password validation
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_REDIRECT_URL = "/menu"

LOGOUT_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGES += [("es-pe", "Peruvian Spanish")]

LANGUAGE_CODE = "es-pe"

TIME_ZONE = "America/Lima"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT_DEFAULT = str(ROOT_DIR / "static")

STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=STATIC_ROOT_DEFAULT)
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = env.str("DJANGO_STATIC_URL", default="/static/")
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]

# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT_DEFAULT = str(ROOT_DIR / "media")

MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default=MEDIA_ROOT_DEFAULT)
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = env.str("DJANGO_MEDIA_URL", default="/media/")

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

SITE_URL = env.str("SITE_URL", "http://localhost:8000")

API_URL = env.str("API_URL", SITE_URL)

# General

APPEND_SLASH = True

# REST

DEFAULT_API_KEYS = {}

ALLOWED_API_KEYS = env.dict("ALLOWED_API_KEYS", default=DEFAULT_API_KEYS)

EMAIL_BACKEND = env.str("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")

EMAIL_HOST = env.str("EMAIL_HOST", None)

EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", True)

DEFAULT_EMAIL_PORT = 587

EMAIL_PORT = env.int("EMAIL_PORT", DEFAULT_EMAIL_PORT)

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", None)

EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", None)

# Apps
PHONENUMBER_DB_FORMAT = "RFC3966"

PHONENUMBER_COUNTRY_PREFIX = "+51"

# Medicos
DEFAULT_COUNTRY = env.str("DEFAULT_COUNTRY", "PE")

# Terms
CURRENT_TERMS_VERSIONS = {"medicos": "1.0", "pacientes": "1.0"}
TERMS_ORGANIZATION = 'Instituto de Enfermedades Tropicales "Alexander Von Humboldt"'

# Consultas
CONSULTAS_CODE_OFFSET_DEFAULT = 10 ** 5

CONSULTAS_CODE_OFFSET = env.int("CONSULTAS_CODE_OFFSET", CONSULTAS_CODE_OFFSET_DEFAULT)

CONSULTAS_CODE_ALPHABET_DEFAULT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

CONSULTAS_CODE_ALPHABET = env("CONSULTAS_CODE_ALPHABET", default=CONSULTAS_CODE_ALPHABET_DEFAULT)

MEDICAL_AVAILABILITY_DAYS = [
    ("monday", _("Lunes")),
    ("tuesday", _("Martes")),
    ("ednesday", _("Miércoles")),
    ("thursday", _("Jueves")),
    ("friday", _("Viernes")),
    ("saturday", _("Sábado")),
]

MEDICAL_AVAILABILITY_SHIFTS = [
    ("morning", _("Mañana")),
    ("evening", _("Tarde")),
    ("night", _("Noche")),
]
