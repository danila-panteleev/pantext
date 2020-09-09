from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = 'v_n3v_8u=b&kl=p@w3=#(05-i8im)j#iafsa8z!0q23flt3w_&'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'main/static/'