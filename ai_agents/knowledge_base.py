import json
from typing import Dict, List

from app.backend.core.logger import logger


class KnowledgeBase:
    def __init__(self, data_file: str = "data/knowledge.json"):
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self) -> List[Dict]:
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} items from knowledge base")
            return data
        except FileNotFoundError:
            logger.warning(f"Knowledge base file not found: {self.data_file}")
            return []

    def search(self, query: str) -> List[Dict]:
        # Simple search implementation. In a real-world scenario, 
        # you might want to use more sophisticated search algorithms or vector databases.
        results = []
        for item in self.data:
            if query.lower() in item.get('content', '').lower():
                results.append(item)
        logger.info(f"Found {len(results)} results for query: {query}")
        return results

    def add_item(self, item: Dict):
        self.data.append(item)
        self._save_data()
        logger.info(f"Added new item to knowledge base: {item}")

    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f)
        logger.info(f"Saved {len(self.data)} items to knowledge base")