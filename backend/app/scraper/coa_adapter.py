import asyncio
import re
import logging
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup
try:
    from app.scraper.adapter import DirectoryAdapter
    from app.scraper.rate_limiter import RateLimiter
    from app.core.config import settings
except ImportError:
    from scraper.adapter import DirectoryAdapter
    from scraper.rate_limiter import RateLimiter
    from core.config import settings

logger = logging.getLogger(__name__)

class CoADirectoryAdapter(DirectoryAdapter):
    """
    Live Council of Architecture (CoA) public directory adapter.
    Extracts server-side rendered architect records from the official public register.
    """
    BASE_URL = settings.COA_BASE_URL
    DIRECTORY_PATH = "/default_arch.php"

    def __init__(self, rate_limiter: RateLimiter, timeout: int = 30, max_retries: int = 3):
        self.rate_limiter = rate_limiter
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": f"{self.BASE_URL}/default_arch.php",
            },
            timeout=float(timeout),
            follow_redirects=True,
            verify=False  # Required for some Indian NIC/gov SSL certificates
        )

    async def fetch_page(self, page: int) -> str:
        """
        Fetch directory page with bounded concurrency, token-bucket rate limiting,
        and exponential backoff on transient network / server faults.
        """
        url = f"{self.DIRECTORY_PATH}?page={page}&lang=1&level=&linkid=&lid="
        
        for attempt in range(1, self.max_retries + 1):
            async with self.rate_limiter.semaphore:
                await self.rate_limiter.acquire()
                try:
                    logger.info(f"Fetching CoA directory page {page} (attempt {attempt}/{self.max_retries})")
                    resp = await self.client.get(url)
                    
                    # Handle Rate Limiting (429)
                    if resp.status_code == 429:
                        retry_after = resp.headers.get("Retry-After")
                        delay = float(retry_after) if retry_after and retry_after.isdigit() else 5.0
                        self.rate_limiter.report_rate_limited(delay)
                        if attempt == self.max_retries:
                            resp.raise_for_status()
                        await asyncio.sleep(delay)
                        continue

                    # Handle server errors (500, 502, 503, 504)
                    if resp.status_code in [500, 502, 503, 504]:
                        logger.warning(f"CoA server error {resp.status_code} on page {page}")
                        if attempt == self.max_retries:
                            resp.raise_for_status()
                        await asyncio.sleep(2.0 ** attempt)
                        continue

                    resp.raise_for_status()
                    self.rate_limiter.report_success()
                    return resp.text

                except (httpx.TimeoutException, httpx.NetworkError) as exc:
                    logger.warning(f"Network error fetching page {page}: {exc}")
                    if attempt == self.max_retries:
                        raise
                    await asyncio.sleep(2.0 ** attempt)

        raise RuntimeError(f"Exhausted retries fetching page {page}")

    def parse_records(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Parse architect table rows from CoA HTML payload.
        Expected columns: Sl., Name, Registration Number, City, Valid up to.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        records = []
        
        # Look for table inside #cmscontent2 or fallback to tables with matching headers
        table = None
        for t in soup.find_all("table"):
            text = t.get_text()
            if "Registration Number" in text and "Valid up to" in text:
                table = t
                break

        if not table:
            logger.warning("No matching architect table found in HTML response")
            return records

        rows = table.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            if len(tds) < 4:
                continue  # Skip header or spacing rows

            try:
                sl_text = tds[0].get_text(strip=True)
                name_text = tds[1].get_text(separator=" ", strip=True)
                reg_no_text = tds[2].get_text(strip=True)
                city_text = tds[3].get_text(strip=True)
                valid_up_to = tds[4].get_text(strip=True) if len(tds) > 4 else None

                # Clean non-breaking spaces and extra spaces
                name_clean = re.sub(r"\s+", " ", name_text.replace("\xa0", " ")).strip()
                reg_clean = reg_no_text.replace("\xa0", " ").strip().upper()
                city_clean = city_text.replace("\xa0", " ").strip()

                if not reg_clean or not name_clean:
                    continue

                records.append({
                    "serial_no": sl_text,
                    "registration_number": reg_clean,
                    "name": name_clean,
                    "city": city_clean,
                    "valid_up_to": valid_up_to,
                    "raw_data": {
                        "sl": sl_text,
                        "name": name_text,
                        "reg_no": reg_no_text,
                        "city": city_text,
                        "valid_up_to": valid_up_to,
                        "source": "CoA Public Register (default_arch.php)"
                    }
                })
            except Exception as e:
                logger.error(f"Error parsing table row: {e}")
                continue

        return records

    def get_total_pages(self, html_content: str) -> Optional[int]:
        """Extract total page count from pagination anchor tags."""
        soup = BeautifulSoup(html_content, "html.parser")
        max_page = 1
        for a in soup.find_all("a", href=True):
            href = a["href"]
            match = re.search(r"page=(\d+)", href)
            if match:
                page_val = int(match.group(1))
                if page_val > max_page:
                    max_page = page_val
        return max_page if max_page > 1 else None

    async def close(self):
        await self.client.aclose()
