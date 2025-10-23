"""
Pytest configuration and shared fixtures for docprocessor tests.
"""

import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture
def tmp_path():
    """Provide a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text():
    """Provide sample text for testing."""
    return """
    Artificial Intelligence and Machine Learning

    Artificial intelligence (AI) is intelligence demonstrated by machines,
    as opposed to natural intelligence displayed by humans or animals.

    Machine learning is a subset of artificial intelligence that provides
    systems the ability to automatically learn and improve from experience
    without being explicitly programmed.

    Deep learning is part of a broader family of machine learning methods
    based on artificial neural networks with representation learning.

    Applications of AI include natural language processing, computer vision,
    robotics, and autonomous vehicles.
    """


@pytest.fixture
def sample_txt_file(tmp_path, sample_text):
    """Create a sample .txt file for testing."""
    file_path = tmp_path / "sample.txt"
    file_path.write_text(sample_text)
    return file_path


@pytest.fixture
def long_text():
    """Provide longer text for chunking tests."""
    paragraphs = [f"This is paragraph number {i}. " * 50 for i in range(20)]
    return "\n\n".join(paragraphs)


@pytest.fixture
def mock_llm_client():
    """Mock LLM client for testing."""

    class MockLLMClient:
        def complete_chat(self, messages: list, temperature: float = 0.3) -> Dict[str, Any]:
            """Mock LLM completion."""
            return {"content": "This is a mock summary of the document content."}

    return MockLLMClient()


@pytest.fixture
def pdf_with_text_content(tmp_path):
    """Create a minimal PDF with text content for testing."""
    # Note: This requires reportlab, which should be added as a dev dependency
    # For now, we'll skip this fixture if reportlab is not available
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        pdf_path = tmp_path / "sample.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 700, "This is a test PDF with some text content.")
        c.drawString(100, 650, "It contains multiple lines of text.")
        c.showPage()
        c.save()

        return pdf_path
    except ImportError:
        pytest.skip("reportlab not installed, skipping PDF fixture")


@pytest.fixture
def mock_meilisearch_client():
    """Mock Meilisearch client for testing."""

    class MockIndex:
        def __init__(self, name):
            self.name = name
            self.documents = []
            self.settings = {}

        def add_documents(self, documents, primary_key=None):
            self.documents.extend(documents)
            return {"status": "enqueued", "taskUid": 1}

        def search(self, query, options=None):
            # Extract limit from options if provided
            limit = options.get("limit", 20) if options else 20
            return {"hits": [], "limit": limit, "offset": 0}

        def delete_document(self, doc_id):
            return {"status": "enqueued", "taskUid": 2}

        def delete_documents(self, filter_dict):
            return {"status": "enqueued", "taskUid": 3}

        def update_settings(self, settings):
            self.settings.update(settings)
            return {"status": "enqueued", "taskUid": 4}

    class MockClient:
        def __init__(self):
            self.indexes = {}

        def index(self, name):
            """Get or create an index (used by MeiliSearchIndexer)."""
            if name not in self.indexes:
                self.indexes[name] = MockIndex(name)
            return self.indexes[name]

        def get_index(self, name):
            """Get an existing index."""
            if name not in self.indexes:
                self.indexes[name] = MockIndex(name)
            return self.indexes[name]

        def create_index(self, name, options=None):
            self.indexes[name] = MockIndex(name)
            return {"status": "enqueued", "taskUid": 0}

    return MockClient()
