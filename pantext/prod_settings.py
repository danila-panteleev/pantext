from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v_n3v_#@RFEr23rgfgfdg5645rtujkuyjlp[luikyhgjfj#iaffgfgwr23rvds8z!0q23flt3w_&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

STATIC_DIR = os.path.join(BASE_DIR, 'main/static')
STATIC_ROOT = os.path.join(BASE_DIR, 'main/static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postresql.psycopg2',
        'NAME': 'pantext',
        'USER': 'pantextdb',
        'PASSWORD': '130013',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}