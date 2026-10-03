"""Web crawlers for Turkish networking hardware markets"""
from .epey import crawl_epey
from .akakce import crawl_akakce

__all__ = ["crawl_epey", "crawl_akakce"]
