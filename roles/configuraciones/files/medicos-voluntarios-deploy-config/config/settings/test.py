"""
With these settings, tests run faster.
"""

import logging

from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="WNjRfgUC564SMNg8Vb3SVXnw6OO6matU5U5qZwomt6ylQSpnKiZXAMeclDCapAW8",)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "",}}

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader",],
    )
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------

# Disable invalid request logging using django's test client
# https://stackoverflow.com/questions/6377231/avoid-warnings-on-404-during-django-test-runs
logging.getLogger("django.request").setLevel(logging.ERROR)
