from .settings import *

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_DIR / 'db.sqlite3',
        }
    }
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"