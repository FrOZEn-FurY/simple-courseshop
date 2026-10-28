import shortuuid
import requests
import os

from django.conf import settings

from dotenv import load_dotenv

from .models import Token

load_dotenv(settings.BASE_DIR / '.env')

def send_otp(phone_number):
    s = shortuuid.ShortUUID(alphabet='0123456789')
    token = s.random(5)
    Token.objects.create(value=token)
    url = 'https://api.sms.ir/v1/send/verify'
    data = {
        "mobile": phone_number.as_e164,
        "templateId": "135638",
        "parameters": [
            {
                "name": "CODE",
                "value": token
            }
        ]
    }
    headers = {
        "Accept": "application/json",
        "X-API-KEY": os.getenv("SMS_PANEL_API_KEY", None)
    }
    response = requests.post(url, json=data, headers=headers)
    return response