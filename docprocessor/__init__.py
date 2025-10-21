"""
Document Processor Library

A Python library for processing documents with OCR, chunking, and summarization capabilities.
Designed for semantic search and document analysis workflows.
"""

__version__ = "0.1.0"

from .processor import DocumentProcessor
from .integrations.meilisearch_indexer import MeiliSearchIndexer
from .core.chunker import DocumentChunk

__all__ = [
    "DocumentProcessor",
    "MeiliSearchIndexer",
    "DocumentChunk",
]
