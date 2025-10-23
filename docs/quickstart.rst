Quick Start Guide
=================

This guide will help you get started with docprocessor in minutes.

Basic Usage
-----------

Simple Text Extraction
~~~~~~~~~~~~~~~~~~~~~~

Extract text from any supported document:

.. code-block:: python

    from docprocessor import DocumentProcessor

    # Initialize processor
    processor = DocumentProcessor()

    # Extract text
    result = processor.extract_text("document.pdf")

    print(f"Text: {result['text']}")
    print(f"Pages: {result['page_count']}")
    print(f"Format: {result['metadata']['format']}")

Text Extraction and Chunking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract and chunk a document for semantic search:

.. code-block:: python

    from docprocessor import DocumentProcessor

    processor = DocumentProcessor(
        chunk_size=512,
        chunk_overlap=50
    )

    result = processor.process(
        file_path="document.pdf",
        extract_text=True,
        chunk=True
    )

    print(f"Created {len(result.chunks)} chunks")

    for i, chunk in enumerate(result.chunks):
        print(f"Chunk {i}: {chunk.chunk_text[:100]}...")

With LLM Summarization
~~~~~~~~~~~~~~~~~~~~~~

Add AI-powered summarization:

.. code-block:: python

    from docprocessor import DocumentProcessor

    # Your LLM client (must implement complete_chat method)
    class MyLLMClient:
        def complete_chat(self, messages, temperature=0.3):
            # Call your LLM provider (OpenAI, Anthropic, etc.)
            response = your_llm_api.chat(messages, temperature)
            return {"content": response.text}

    llm_client = MyLLMClient()

    processor = DocumentProcessor(
        llm_client=llm_client,
        summary_target_words=200
    )

    result = processor.process(
        file_path="document.pdf",
        extract_text=True,
        chunk=True,
        summarize=True
    )

    print(f"Summary: {result.summary}")

Complete Pipeline with Meilisearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Full pipeline from document to searchable index:

.. code-block:: python

    from docprocessor import DocumentProcessor, MeiliSearchIndexer

    # Initialize
    processor = DocumentProcessor(llm_client=your_llm)
    indexer = MeiliSearchIndexer(
        url="http://localhost:7700",
        api_key="your_master_key",
        index_prefix="prod_"
    )

    # Process document
    result = processor.process(
        file_path="document.pdf",
        extract_text=True,
        chunk=True,
        summarize=True,
        file_id="doc-123",
        project_id=456
    )

    # Index chunks for search
    search_docs = processor.chunks_to_search_documents(result.chunks)
    indexer.index_chunks(search_docs, 'document_chunks')

    # Index document metadata
    doc_metadata = {
        'id': 'doc-123',
        'filename': 'document.pdf',
        'summary': result.summary,
        'chunk_count': len(result.chunks),
        'page_count': result.page_count
    }
    indexer.index_document(doc_metadata, 'documents')

    # Search
    results = indexer.search(
        query="artificial intelligence",
        index_name="document_chunks",
        limit=10
    )

    for hit in results['hits']:
        print(f"Match: {hit['chunk_preview']}")

Supported File Formats
----------------------

docprocessor supports the following formats:

* **PDF** (.pdf) - with OCR fallback
* **Word** (.docx) - using python-docx
* **Text** (.txt, .md) - direct read
* **Images** (.png, .jpg, .jpeg, .gif, .bmp) - using Tesseract OCR

Common Patterns
---------------

Pattern 1: Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Process multiple documents efficiently:

.. code-block:: python

    from pathlib import Path

    processor = DocumentProcessor()
    results = []

    for file_path in Path("documents").glob("*.pdf"):
        result = processor.process(
            file_path=file_path,
            extract_text=True,
            chunk=True
        )
        results.append(result)

    print(f"Processed {len(results)} documents")

Pattern 2: Custom Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add custom metadata to chunks:

.. code-block:: python

    result = processor.process(
        file_path="report.pdf",
        extract_text=True,
        chunk=True,
        file_id="report-2024-q1",
        project_id=789,
        extraction_metadata={
            "author": "John Doe",
            "department": "Research",
            "date": "2024-01-15"
        }
    )

Pattern 3: Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle processing errors gracefully:

.. code-block:: python

    from docprocessor.core.extractor import ContentExtractionError

    processor = DocumentProcessor()

    try:
        result = processor.process("document.pdf")
    except ContentExtractionError as e:
        print(f"Extraction failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

Configuration Options
---------------------

DocumentProcessor Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    processor = DocumentProcessor(
        ocr_enabled=True,           # Enable OCR for PDFs/images
        chunk_size=512,             # Target chunk size (tokens)
        chunk_overlap=50,           # Overlap between chunks (tokens)
        min_chunk_size=100,         # Minimum chunk size (tokens)
        summary_target_words=500,   # Target summary length (words)
        llm_client=your_llm,        # Optional LLM client
        llm_temperature=0.3         # LLM temperature (0.0-1.0)
    )

MeiliSearchIndexer Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    indexer = MeiliSearchIndexer(
        url="http://localhost:7700",   # Meilisearch URL
        api_key="your_key",             # API key
        index_prefix="prod_"            # Optional prefix for multi-env
    )

Next Steps
----------

* Read the :doc:`usage` guide for detailed explanations
* Check :doc:`advanced` for advanced features
* See :doc:`api/processor` for complete API reference
* Browse the `examples <https://github.com/Knowledge-Innovation-Centre/doc-processor/tree/main/examples>`_ directory

Common Issues
-------------

**"Tesseract not found"**
    Install Tesseract OCR: ``sudo apt-get install tesseract-ocr``

**"No chunks created"**
    Document might be too short. Reduce ``min_chunk_size`` parameter.

**"LLM summarization failed"**
    Ensure your LLM client implements ``complete_chat(messages, temperature)``

**Import errors**
    Install all dependencies: ``pip install -e ".[dev]"``

For more help, see :doc:`installation` or ask in our `GitHub Discussions <https://github.com/Knowledge-Innovation-Centre/doc-processor/discussions>`_.
