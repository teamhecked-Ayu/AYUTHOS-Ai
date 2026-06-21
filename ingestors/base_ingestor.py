from typing import Dict, Any, List

class BaseIngestor:
    def __init__(self, name: str):
        self.name = name

    async def fetch(self) -> List[Dict[str, Any]]:
        """Abstract method to fetch data from a source."""
        raise NotImplementedError("Subclasses must implement the fetch method")

    def parse(self, raw_data: Any) -> List[Dict[str, Any]]:
        """Abstract method to parse raw data into a standardized format."""
        raise NotImplementedError("Subclasses must implement the parse method")

    async def ingest(self) -> List[Dict[str, Any]]:
        raw_data = await self.fetch()
        processed_data = self.parse(raw_data)
        return processed_data
