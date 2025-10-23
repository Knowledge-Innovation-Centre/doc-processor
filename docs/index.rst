Welcome to docprocessor's documentation!
==========================================

**docprocessor** is a Python library for intelligent document processing with OCR, semantic chunking, and AI-powered summarization.

.. image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

Features
--------

* **Multi-format Support**: PDF, DOCX, TXT, MD, and images
* **Intelligent OCR**: Layout-aware extraction with fallback
* **Semantic Chunking**: Token-based text segmentation
* **LLM Summarization**: BYOC (Bring Your Own Client) pattern
* **Meilisearch Integration**: Built-in search engine support
* **Flexible API**: Use components individually or together

Quick Start
-----------

Installation::

    pip install docprocessor

Basic usage:

.. code-block:: python

    from docprocessor import DocumentProcessor

    # Initialize processor
    processor = DocumentProcessor()

    # Process a document
    result = processor.process(
        file_path="document.pdf",
        extract_text=True,
        chunk=True,
        summarize=False
    )

    print(f"Extracted {len(result.text)} characters")
    print(f"Created {len(result.chunks)} chunks")

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   usage
   advanced

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/processor
   api/extractor
   api/chunker
   api/summarizer
   api/meilisearch

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   contributing
   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
