DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hackernews_clone',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': ''
    }
}

ALLOWED_HOSTS = ['*']
