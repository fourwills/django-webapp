""" Get Environment Variables """
import os

OAUTH_CONSUMER_KEY = os.environ.get(
    'OAUTH_CONSUMER_KEY', None)
OAUTH_CONSUMER_SECRET = os.environ.get(
    'OAUTH_CONSUMER_SECRET', None)
OAUTH_TOKEN = os.environ.get(
    'OAUTH_TOKEN', None)
OAUTH_TOKEN_SECRET = os.environ.get(
    'OAUTH_TOKEN_SECRET', None)
