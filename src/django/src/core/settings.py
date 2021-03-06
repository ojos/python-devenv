"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Environment variables

APP_ENV = os.getenv("APP_ENV", "local-dev")
MYSQL_PRIMARY_HOST = os.getenv("MYSQL_PRIMARY_HOST", "ojos-python.db")
MYSQL_REPLICA_HOST = os.getenv("MYSQL_REPLICA_HOST", "ojos-python.db")
MYSQL_USER = os.getenv("MYSQL_USER", "ojos")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "ojos")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ojos")
CACHE_HOST = os.getenv("CACHE_HOST", "ojos-python.cache")
STATIC_URL = os.getenv("STATIC_URL", "/static/")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "ml@0(zynwl-y^i9hd97g82@c()$wok+zhp)b-se47%lb4jyx#*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = APP_ENV != "production"
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
if APP_ENV != "production":
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_DATABASE,
        "USER": MYSQL_USER,
        "PASSWORD": MYSQL_PASSWORD,
        "HOST": MYSQL_PRIMARY_HOST,
        "PORT": "3306",
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    "replica": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_DATABASE,
        "USER": MYSQL_USER,
        "PASSWORD": MYSQL_PASSWORD,
        "HOST": MYSQL_REPLICA_HOST,
        "PORT": "3306",
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}
DATABASE_ROUTERS = ["core.router.Router"]


# Cache
# https://docs.djangoproject.com/en/3.1/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:6379/0".format(CACHE_HOST),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_TIMEOUT": 5,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Media
# https://docs.djangoproject.com/en/3.1/topics/files/

MEDIA_ROOT = "{}/media/".format(BASE_DIR)
MEDIA_URL = "/media/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = "{}/static/".format(BASE_DIR)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# Admin

ADMIN_SITE_TITLE = ""
ADMIN_SITE_HEADER = ""
ADMIN_SITE_INDEX_TITLE = ""
ADMIN_SITE_URL = "/__admin__/"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s a",
        },
        # プロジェクト用のフォーマットを追加
        "heibon": {
            "format": "\t".join(
                [
                    "[%(levelname)s]",
                    "%(asctime)s",
                    "%(name)s:%(lineno)d",
                    "%(message)s",
                    "%(threadName)s",
                ]
            )
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "heibon",  # フォーマッター追加
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "DEBUG",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "DEBUG",
            "propagate": False,
        },
        "app": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "ojos_ca": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
