import asyncio
import time
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Token-bucket async rate limiter with dynamic backoff and Retry-After support.
    Safely constrains requests/second and manages adaptive backoff on HTTP 429.
    """
    def __init__(self, requests_per_second: float = 2.0, max_concurrency: int = 5):
        self.rate = max(0.2, requests_per_second)
        self.capacity = float(self.rate)
        self.tokens = self.capacity
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.backoff_until = 0.0
        self.consecutive_429_count = 0

    async def acquire(self):
        """Wait until a rate limit token is available and any backoff has elapsed."""
        async with self.lock:
            # Check if we are currently backing off due to a 429
            now = time.monotonic()
            if now < self.backoff_until:
                sleep_duration = self.backoff_until - now
                logger.warning(f"RateLimiter active backoff: sleeping for {sleep_duration:.2f}s")
                await asyncio.sleep(sleep_duration)
                now = time.monotonic()

            # Replenish tokens
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens < 1.0:
                wait_time = (1.0 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0.0
                self.last_update = time.monotonic()
            else:
                self.tokens -= 1.0

    def report_rate_limited(self, retry_after: float = None):
        """Handle 429 response: increase backoff and temporarily throttle rate."""
        self.consecutive_429_count += 1
        now = time.monotonic()
        if retry_after is not None and retry_after > 0:
            delay = retry_after
        else:
            delay = min(2.0 ** self.consecutive_429_count, 30.0)
        self.backoff_until = now + delay
        # Dynamically reduce rate if repeated 429s occur
        if self.consecutive_429_count > 2:
            self.rate = max(0.5, self.rate * 0.7)
            self.capacity = self.rate
        logger.warning(f"Rate limit triggered. Consecutive: {self.consecutive_429_count}, backing off {delay:.1f}s, new rate: {self.rate:.2f} req/s")

    def report_success(self):
        """Reset consecutive rate limit penalty counter on healthy response."""
        if self.consecutive_429_count > 0:
            self.consecutive_429_count = max(0, self.consecutive_429_count - 1)
