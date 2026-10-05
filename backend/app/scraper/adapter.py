from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DirectoryAdapter(ABC):
    """Abstract interface for Council of Architecture directory scrapers."""

    @abstractmethod
    async def fetch_page(self, page: int) -> str:
        """Fetch raw HTML for the specified page number."""
        pass

    @abstractmethod
    def parse_records(self, html_content: str) -> List[Dict[str, Any]]:
        """Parse raw HTML into un-normalized structured records."""
        pass

    @abstractmethod
    def get_total_pages(self, html_content: str) -> Optional[int]:
        """Discover total number of pages from pagination controls."""
        pass

    @abstractmethod
    async def close(self):
        """Clean up network sessions and connection pools."""
        pass
