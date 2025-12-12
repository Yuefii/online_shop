from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from api.core.limiter import limiter
from api.routers import auth, user, categories, products


api = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
api.add_middleware(SlowAPIMiddleware)


api.include_router(auth.router, prefix="/auth", tags=["Auth"])
api.include_router(user.router, prefix="/users", tags=["Users"])
api.include_router(categories.router, prefix="/categories", tags=["Categories"])
api.include_router(products.router, prefix="/products", tags=["Products"])