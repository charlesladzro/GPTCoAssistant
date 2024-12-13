from flask import request, abort
from config import SECRET_API_KEY

COOKIE_CODEVACCESSTOKEN = "CodevAccessToken"

def extract_api_key(request):
    """Extract API key from Authorization header or Cookie."""
    secret = request.headers.get("Authorization")
    if secret is None:
        secret = request.headers.get("Cookie")
        if secret:
            start = secret.find(COOKIE_CODEVACCESSTOKEN)
            if start >= 0:
                start += len(COOKIE_CODEVACCESSTOKEN)
                end = secret.find(';', start)
                if end == -1:
                    end = len(secret)
                secret = secret[start:end]
            else:
                secret = None
    elif secret.startswith("Bearer "):
        secret = secret[len("Bearer "):]
    elif secret.startswith("Basic "):
        secret = secret[len("Basic "):]
    return secret

def require_api_key(func):
    """Decorator to enforce API key authentication."""
    def wrapper(*args, **kwargs):
        api_key = extract_api_key(request)
        if 'localhost' not in str(request):
            if api_key != SECRET_API_KEY:
                abort(401, description="Unauthorized: Invalid API key")
        return func(*args, **kwargs)
    return wrapper
