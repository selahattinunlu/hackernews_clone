"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

environment = os.environ.get('ENV') if 'ENV' in os.environ else 'dev'

from settings.base import *

if environment == 'dev':
    from settings.dev import *

if environment == 'production':
    from settings.production import *

