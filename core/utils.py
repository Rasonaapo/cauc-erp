
import time
import requests
import urllib.parse
from django.conf import settings

LOCKOUT_PERIOD = 60 * 60  # 1 hour in seconds

def format_phone_number(phone_number):
        """Format the phone number to (XXX)-XXXX-XXX format."""
        if phone_number and len(phone_number) == 10:
            return f"({phone_number[:3]})-{phone_number[3:7]}-{phone_number[7:]}"
        return phone_number  # Return unformatted if not 10 digits


def is_locked_out(request):
    lockout_time = request.session.get('reg_lockout_time')
    if not lockout_time:
        return False
    elapsed = time.time() - lockout_time
    if elapsed < LOCKOUT_PERIOD:
        return True
    # Lockout expired, clear it
    request.session['reg_attempts'] = 0
    request.session['reg_lockout_time'] = None
    return False


def send_sms(msg, contact):
    """
    Sends an SMS using mNotify SMS gateway.
    Reads API key and sender ID from settings.py.
    """
    api_key = getattr(settings, "MNOTIFY_API_KEY", None)
    sender_id = getattr(settings, "MNOTIFY_SENDER_ID", "CAUC")

    if not api_key:
        return {"error": "API key not set in settings.py"}

    sms = urllib.parse.quote(msg)
    url = (
        f"https://apps.mnotify.net/smsapi?"
        f"key={api_key}&to={contact}&msg={sms}&sender_id={sender_id}"
    )

    try:
        response = requests.get(url, timeout=10)
        try:
            return response.json()
        except Exception:
            return {"raw_response": response.text}
    except requests.RequestException as e:
        return {"error": str(e)}
    