import asyncio
import json
import os
from typing import List, Dict, Any, Optional
try:
    from app.scraper.adapter import DirectoryAdapter
    from app.scraper.rate_limiter import RateLimiter
except ImportError:
    from scraper.adapter import DirectoryAdapter
    from scraper.rate_limiter import RateLimiter

class MockDirectoryAdapter(DirectoryAdapter):
    """
    Offline mock adapter serving realistic Council of Architecture records
    from mock_data/architects.json. Enables reliable offline demonstrations and testing.
    """
    def __init__(self, rate_limiter: RateLimiter, page_size: int = 50, simulated_delay: float = 0.15):
        self.rate_limiter = rate_limiter
        self.page_size = page_size
        self.simulated_delay = simulated_delay
        self.records: List[Dict[str, Any]] = []
        
        # Load mock dataset
        mock_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "mock_data", "architects.json")
        if os.path.exists(mock_file):
            with open(mock_file, "r", encoding="utf-8") as f:
                self.records = json.load(f)

    async def fetch_page(self, page: int) -> str:
        """Simulate async network fetch with rate limiting and realistic delay."""
        async with self.rate_limiter.semaphore:
            await self.rate_limiter.acquire()
            if self.simulated_delay > 0:
                await asyncio.sleep(self.simulated_delay)
            self.rate_limiter.report_success()
            return f"<!-- MOCK PAGE {page} WITH {len(self.records)} TOTAL RECORDS -->"

    def parse_records(self, html_content: str) -> List[Dict[str, Any]]:
        """Slice mock records based on requested page number."""
        import re
        match = re.search(r"MOCK PAGE (\d+)", html_content)
        page = int(match.group(1)) if match else 1
        
        start_idx = (page - 1) * self.page_size
        end_idx = start_idx + self.page_size
        
        if not self.records:
            return []
            
        # Loop over mock records if page exceeds length
        total = len(self.records)
        selected = []
        for i in range(start_idx, end_idx):
            record = dict(self.records[i % total])
            # Modify serial to match page
            record["serial_no"] = i + 1
            selected.append(record)
            
        return selected

    def get_total_pages(self, html_content: str) -> Optional[int]:
        return max(1, (len(self.records) + self.page_size - 1) // self.page_size)

    async def close(self):
        pass
