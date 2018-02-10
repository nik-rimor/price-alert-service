import os

URL = os.getenv('MAILGUN_URL')
API_KEY = os.getenv('MAILGUN_API_KEY')
FROM = os.getenv('MAILGUN_FROM')

COLLECTION="alerts"
ALERT_TIMEOUT = 10