from .base import *

SECRET_KEY = env.str("SECRET_KEY", default="random-string-but-you-better-set-it")

ALLOWED_HOSTS_DEFAULT = ["localhost", "0.0.0.0", "127.0.0.1"]

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=ALLOWED_HOSTS_DEFAULT)

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "",}}

EMAIL_BACKEND = env.str("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

INSTALLED_APPS += [
    "debug_toolbar",  # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
]  # noqa F405

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "request_logging.middleware.LoggingMiddleware",
]  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler",},},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",  # change debug level as appropiate
            "propagate": False,
        },
    },
}
