import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reuters_com')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'reuters_com.settings'

django.setup()