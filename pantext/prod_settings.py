from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

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
