from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from api.core.limiter import limiter
from api.routers import auth, user


api = FastAPI()
api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
api.add_middleware(SlowAPIMiddleware)


api.include_router(auth.router, prefix="/auth", tags=["Auth"])
api.include_router(user.router, prefix="/users", tags=["Users"])