from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

def get_real_ip(request: Request):
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"]
    return get_remote_address(request)

limiter = Limiter(key_func=get_real_ip)
