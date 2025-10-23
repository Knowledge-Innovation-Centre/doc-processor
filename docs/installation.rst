Installation
============

Requirements
------------

* Python 3.8 or higher
* Tesseract OCR (for image processing)
* Poppler (for PDF to image conversion)

System Dependencies
-------------------

Ubuntu/Debian
~~~~~~~~~~~~~

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install tesseract-ocr tesseract-ocr-eng poppler-utils

macOS
~~~~~

.. code-block:: bash

    brew install tesseract poppler

Windows
~~~~~~~

Download and install:

* `Tesseract OCR <https://github.com/UB-Mannheim/tesseract/wiki>`_
* `Poppler for Windows <https://github.com/oschwartz10612/poppler-windows/releases/>`_

Install from PyPI
-----------------

The recommended way to install docprocessor is via pip:

.. code-block:: bash

    pip install docprocessor

Install from GitHub
-------------------

To install the latest development version:

.. code-block:: bash

    pip install git+https://github.com/Knowledge-Innovation-Centre/doc-processor.git

Development Installation
------------------------

For development, clone the repository and install in editable mode:

.. code-block:: bash

    git clone https://github.com/Knowledge-Innovation-Centre/doc-processor.git
    cd doc-processor
    pip install -e ".[dev]"

This installs docprocessor along with development dependencies including pytest, black, and mypy.

Optional Dependencies
---------------------

Meilisearch Integration
~~~~~~~~~~~~~~~~~~~~~~~

Meilisearch is installed by default. If you don't need it:

.. code-block:: bash

    pip install docprocessor --no-deps
    pip install pdfminer.six pdf2image pytesseract opencv-python Pillow python-docx langchain-text-splitters tiktoken

Development Tools
~~~~~~~~~~~~~~~~~

For running tests and code quality checks:

.. code-block:: bash

    pip install docprocessor[dev]

Documentation
~~~~~~~~~~~~~

For building documentation:

.. code-block:: bash

    pip install docprocessor[docs]

Verification
------------

Verify your installation:

.. code-block:: python

    from docprocessor import DocumentProcessor
    print("docprocessor installed successfully!")

Check system dependencies:

.. code-block:: bash

    # Check Tesseract
    tesseract --version

    # Check Poppler
    pdfinfo -v

Troubleshooting
---------------

Import Errors
~~~~~~~~~~~~~

If you encounter import errors, ensure all system dependencies are installed:

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install tesseract-ocr poppler-utils

Tesseract Not Found
~~~~~~~~~~~~~~~~~~~

If you see "TesseractNotFoundError":

1. Verify Tesseract is installed: ``tesseract --version``
2. On Windows, add Tesseract to your PATH
3. Set TESSDATA_PREFIX environment variable if needed

PDF Processing Errors
~~~~~~~~~~~~~~~~~~~~~

If PDF processing fails:

1. Verify Poppler is installed: ``pdfinfo -v``
2. Check PDF file is not corrupted
3. Try with a different PDF file

Memory Issues
~~~~~~~~~~~~~

For large documents:

1. Process documents in smaller batches
2. Increase system memory
3. Reduce chunk size to lower memory usage

Getting Help
------------

If you encounter issues:

* Check the `GitHub Issues <https://github.com/Knowledge-Innovation-Centre/doc-processor/issues>`_
* Ask in `GitHub Discussions <https://github.com/Knowledge-Innovation-Centre/doc-processor/discussions>`_
* Email: info@knowledgeinnovation.eu
