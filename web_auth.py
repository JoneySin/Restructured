import hmac
import time
import hashlib
from aiohttp import web

from config import WEB_USERNAME, WEB_PASSWORD, SECRET_KEY

SESSION_MAX_AGE = 7 * 24 * 3600  # 7 दिन तक login याद रखो


def _sign(value: str) -> str:
    return hmac.new(SECRET_KEY.encode(), value.encode(), hashlib.sha256).hexdigest()


def create_session_token() -> str:
    """Login सफल होने पर एक signed cookie token बनाओ"""
    expiry = str(int(time.time()) + SESSION_MAX_AGE)
    return f"{expiry}.{_sign(expiry)}"


def is_valid_session(token: str) -> bool:
    """Cookie से आया token असली है और अभी तक expire नहीं हुआ, ये चेक करो"""
    try:
        expiry, sig = token.split(".", 1)
    except (ValueError, AttributeError):
        return False
    if not hmac.compare_digest(sig, _sign(expiry)):
        return False
    return int(expiry) > int(time.time())


def check_credentials(username: str, password: str) -> bool:
    return hmac.compare_digest(username or "", WEB_USERNAME) and hmac.compare_digest(password or "", WEB_PASSWORD)


def login_required(handler):
    """Route decorator — बिना valid session cookie के /login पर redirect कर देगा"""
    async def wrapper(request):
        token = request.cookies.get("session", "")
        if not is_valid_session(token):
            raise web.HTTPFound("/login")
        return await handler(request)
    return wrapper
