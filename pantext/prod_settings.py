from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '142.93.131.80', 'pantext.ru', 'www.pantext.ru', 'localhost']

STATIC_DIR = os.path.join(BASE_DIR, '/static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pantext',
        'USER': 'pantextdb',
        'PASSWORD': '13pont13',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
