from time import time
from typing import Dict, List

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Basic in-memory rate limiting middleware."""

    def __init__(self, app, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.buckets: Dict[str, List[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.headers.get("x-forwarded-for")
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        now = time()
        window_start = now - self.window_seconds
        bucket = self.buckets.setdefault(client_ip, [])
        bucket[:] = [timestamp for timestamp in bucket if timestamp > window_start]

        if len(bucket) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests, please try again later.",
            )

        bucket.append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(max(0, self.max_requests - len(bucket)))
        response.headers["X-RateLimit-Reset"] = str(int(window_start + self.window_seconds))
        return response
