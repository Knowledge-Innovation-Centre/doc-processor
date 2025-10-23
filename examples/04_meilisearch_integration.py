"""
Example 04: Meilisearch Integration with docprocessor

This example demonstrates:
- Complete indexing pipeline
- Two-index architecture (chunks + documents)
- Searching and filtering results
- Index management
"""

import os
from pathlib import Path

from docprocessor import DocumentProcessor, MeiliSearchIndexer


def check_meilisearch_connection(url: str, api_key: str) -> bool:
    """Check if Meilisearch is available."""
    try:
        indexer = MeiliSearchIndexer(url=url, api_key=api_key)
        return True
    except Exception as e:
        print(f"Cannot connect to Meilisearch: {e}")
        return False


def example_basic_indexing():
    """Demonstrate basic document indexing."""
    print("=" * 60)
    print("Example 1: Basic Document Indexing")
    print("=" * 60)

    # Configuration
    url = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
    api_key = os.getenv("MEILISEARCH_API_KEY", "masterKey")

    if not check_meilisearch_connection(url, api_key):
        print("\nSkipping: Meilisearch not available")
        print("Start Meilisearch with: docker run -p 7700:7700 getmeili/meilisearch")
        return

    # Initialize
    processor = DocumentProcessor()
    indexer = MeiliSearchIndexer(url=url, api_key=api_key)

    # Create sample document
    sample_text = """
    Introduction to Machine Learning

    Machine learning is a subset of artificial intelligence that enables
    computers to learn from data without being explicitly programmed.

    Key concepts include:
    - Supervised learning: Training on labeled data
    - Unsupervised learning: Finding patterns in unlabeled data
    - Reinforcement learning: Learning through trial and error

    Applications are widespread, from recommendation systems to autonomous
    vehicles, medical diagnosis, and natural language processing.
    """

    temp_file = Path("ml_intro.txt")
    temp_file.write_text(sample_text)

    try:
        # Process document
        result = processor.process(
            file_path=temp_file,
            extract_text=True,
            chunk=True,
            file_id="doc-001",
            output_id="output-001",
            project_id=1,
        )

        print(f"\nProcessed document: {temp_file.name}")
        print(f"Created {len(result.chunks)} chunks")

        # Convert chunks to search documents
        search_docs = processor.chunks_to_search_documents(result.chunks)

        # Index chunks
        index_result = indexer.index_chunks(
            chunks=search_docs, index_name="document_chunks", primary_key="id"
        )

        print(f"\nIndexed to Meilisearch:")
        print(f"  Index: document_chunks")
        print(f"  Documents: {len(search_docs)}")
        print(f"  Status: {index_result}")

    finally:
        temp_file.unlink()


def example_two_index_architecture():
    """Demonstrate two-index architecture (chunks + documents)."""
    print("\n" + "=" * 60)
    print("Example 2: Two-Index Architecture")
    print("=" * 60)

    url = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
    api_key = os.getenv("MEILISEARCH_API_KEY", "masterKey")

    if not check_meilisearch_connection(url, api_key):
        print("\nSkipping: Meilisearch not available")
        return

    processor = DocumentProcessor()
    indexer = MeiliSearchIndexer(url=url, api_key=api_key)

    # Create sample documents
    documents = [
        ("Climate change is affecting global weather patterns. " * 10, "climate.txt"),
        ("Renewable energy sources are becoming more efficient. " * 10, "energy.txt"),
        ("Electric vehicles are reducing carbon emissions. " * 10, "transport.txt"),
    ]

    for i, (text, filename) in enumerate(documents):
        temp_file = Path(filename)
        temp_file.write_text(text)

        try:
            # Process document
            result = processor.process(
                file_path=temp_file,
                extract_text=True,
                chunk=True,
                file_id=f"file-{i+1}",
                output_id=f"output-{i+1}",
                project_id=1,
            )

            # INDEX 1: Document chunks (for semantic search)
            search_docs = processor.chunks_to_search_documents(result.chunks)
            indexer.index_chunks(chunks=search_docs, index_name="document_chunks")

            # INDEX 2: Document metadata (for filtering and overview)
            doc_metadata = {
                "id": f"file-{i+1}",
                "filename": filename,
                "text_length": len(result.text),
                "chunk_count": len(result.chunks),
                "page_count": result.page_count,
                "project_id": 1,
                "indexed_at": "2025-10-22T10:00:00Z",
            }

            indexer.index_document(document=doc_metadata, index_name="documents")

            print(f"\nIndexed: {filename}")
            print(f"  Chunks indexed: {len(search_docs)}")
            print(f"  Metadata indexed: Yes")

        finally:
            temp_file.unlink()


def example_searching():
    """Demonstrate searching indexed documents."""
    print("\n" + "=" * 60)
    print("Example 3: Searching Indexed Documents")
    print("=" * 60)

    url = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
    api_key = os.getenv("MEILISEARCH_API_KEY", "masterKey")

    if not check_meilisearch_connection(url, api_key):
        print("\nSkipping: Meilisearch not available")
        return

    indexer = MeiliSearchIndexer(url=url, api_key=api_key)

    # Search queries
    queries = ["machine learning", "climate change", "renewable energy"]

    for query in queries:
        print(f"\nSearching for: '{query}'")
        print("-" * 60)

        results = indexer.search(query=query, index_name="document_chunks", limit=3)

        if results["hits"]:
            for i, hit in enumerate(results["hits"], 1):
                print(f"\n{i}. {hit.get('filename', 'Unknown')}")
                print(f"   Chunk {hit.get('chunk_number', 0)} of {hit.get('total_chunks', 0)}")
                print(f"   Preview: {hit.get('chunk_preview', '')[:100]}...")
        else:
            print("  No results found")


def example_filtering():
    """Demonstrate filtering search results."""
    print("\n" + "=" * 60)
    print("Example 4: Filtering Search Results")
    print("=" * 60)

    url = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
    api_key = os.getenv("MEILISEARCH_API_KEY", "masterKey")

    if not check_meilisearch_connection(url, api_key):
        print("\nSkipping: Meilisearch not available")
        return

    indexer = MeiliSearchIndexer(url=url, api_key=api_key)

    # Search with filters
    print("\nSearch with project filter:")
    results = indexer.search(
        query="energy", index_name="document_chunks", limit=5, filter="project_id = 1"
    )

    print(f"Found {len(results['hits'])} results for project 1")

    # Search specific file
    print("\nSearch within specific file:")
    results = indexer.search(
        query="climate", index_name="document_chunks", limit=5, filter="file_id = 'file-1'"
    )

    print(f"Found {len(results['hits'])} results in file-1")


def example_index_management():
    """Demonstrate index management operations."""
    print("\n" + "=" * 60)
    print("Example 5: Index Management")
    print("=" * 60)

    url = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
    api_key = os.getenv("MEILISEARCH_API_KEY", "masterKey")

    if not check_meilisearch_connection(url, api_key):
        print("\nSkipping: Meilisearch not available")
        return

    indexer = MeiliSearchIndexer(url=url, api_key=api_key)

    # Create index
    print("\nCreating index...")
    result = indexer.create_index(index_name="test_index", primary_key="id")
    print(f"  Created: {result}")

    # Delete specific document
    print("\nDeleting document...")
    result = indexer.delete_document(document_id="file-1", index_name="documents")
    print(f"  Deleted: {result}")

    # Delete documents by filter
    print("\nDeleting documents by filter...")
    result = indexer.delete_documents_by_filter(
        filter_expression="project_id = 999", index_name="document_chunks"
    )
    print(f"  Deleted: {result}")


def example_multi_environment():
    """Demonstrate multi-environment indexing with prefixes."""
    print("\n" + "=" * 60)
    print("Example 6: Multi-Environment Indexing")
    print("=" * 60)

    url = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
    api_key = os.getenv("MEILISEARCH_API_KEY", "masterKey")

    if not check_meilisearch_connection(url, api_key):
        print("\nSkipping: Meilisearch not available")
        return

    # Different environments
    environments = {
        "dev": MeiliSearchIndexer(url, api_key, index_prefix="dev_"),
        "staging": MeiliSearchIndexer(url, api_key, index_prefix="staging_"),
        "prod": MeiliSearchIndexer(url, api_key, index_prefix="prod_"),
    }

    sample_doc = {"id": "test-doc-1", "filename": "test.txt", "content": "Test document content"}

    for env_name, indexer in environments.items():
        print(f"\nIndexing to {env_name} environment...")

        indexer.index_document(document=sample_doc, index_name="documents")

        # The actual index name will be prefixed
        actual_index = indexer._get_prefixed_index_name("documents")
        print(f"  Indexed to: {actual_index}")


def main():
    """Run all Meilisearch integration examples."""
    print("\n" + "=" * 60)
    print("DOCPROCESSOR - MEILISEARCH INTEGRATION EXAMPLES")
    print("=" * 60)

    print("\nPrerequisites:")
    print("1. Meilisearch running: docker run -p 7700:7700 getmeili/meilisearch")
    print("2. Set MEILISEARCH_URL (default: http://localhost:7700)")
    print("3. Set MEILISEARCH_API_KEY (default: masterKey)")

    try:
        example_basic_indexing()
        example_two_index_architecture()
        example_searching()
        example_filtering()
        example_index_management()
        example_multi_environment()

        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        raise


if __name__ == "__main__":
    main()
