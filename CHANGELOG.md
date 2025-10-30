# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-10-30

### Added
- **PowerPoint (PPTX) support**: Extract text from PowerPoint presentations
  - Text extraction from all slides with slide separators
  - Table content extraction within slides
  - Speaker notes extraction
  - Metadata including slide count, shape count, and table detection
- `python-pptx>=0.6.21` dependency for PPTX processing
- Comprehensive test suite for PPTX extraction (6 new tests):
  - Test for missing dependency handling
  - Test for slide content extraction
  - Test for table extraction
  - Test for speaker notes extraction
  - Test for empty presentations
  - Test for corrupted file handling
- Updated documentation to include PPTX in supported formats

### Changed
- Updated `ContentExtractor` to support `.pptx` file extension
- Enhanced README.md to list PPTX in multi-format support and dependencies

## [Earlier Unreleased]

### Added
- Production-grade test suite with 144 tests and 81% coverage
- Configuration management module with ProcessorConfig and MeiliSearchConfig
- Custom exception hierarchy with 11 exception classes
- Comprehensive test coverage for all core modules:
  - test_config.py (33 tests) - Configuration management with env/file loading
  - test_exceptions.py (27 tests) - Exception hierarchy and inheritance
  - test_extractor.py (18 tests) - Multi-format content extraction
  - test_summarizer.py (17 tests) - AI summarization with fallback
  - test_meilisearch.py (17 tests) - Search integration
  - test_chunker.py (18 tests) - Semantic text chunking
  - test_processor.py (14 tests) - End-to-end document processing
- Dependency injection pattern for MeiliSearchIndexer (better testability)
- Devcontainer configuration for GitHub Codespaces and VS Code Remote Containers
- Modern Python packaging with `pyproject.toml`
- Pre-commit hooks for code quality (Black, isort, flake8, mypy)
- GitHub Actions CI/CD pipeline with multi-Python version testing
- Comprehensive test configuration with coverage reporting
- CONTRIBUTING.md with contribution guidelines
- This CHANGELOG.md file

### Changed
- Enhanced README.md with better documentation
- Improved project structure and organization
- Refactored MeiliSearchIndexer to support dependency injection for testing

## [1.0.0] - 2025-10-22

### Added
- Initial release of docprocessor library
- Multi-format document support (PDF, DOCX, TXT, MD, images)
- Layout-aware PDF extraction with OCR fallback using Tesseract
- Semantic chunking with LangChain's RecursiveCharacterTextSplitter
- Token-based chunking with tiktoken
- AI-powered summarization with BYOC (Bring Your Own Client) pattern
- Meilisearch integration with environment prefix support
- Two-index architecture support (chunks and documents)
- Initial test suite covering core functionality
- ContentExtractor with support for multiple file formats
- DocumentChunker with configurable chunk sizes and overlap
- DocumentSummarizer with customizable temperature and word targets
- MeiliSearchIndexer with batch indexing support
- ProcessResult dataclass for structured results
- DocumentChunk dataclass for chunk metadata

### Features
- **OCR Processing**: Automatic OCR fallback for scanned PDFs and images
- **Multi-format Support**: PDF, DOCX, TXT, MD, PNG, JPG, JPEG
- **Semantic Chunking**: Context-aware text splitting with overlap
- **Metadata Extraction**: Page counts, file info, and custom metadata
- **Flexible Integration**: BYOC pattern allows any LLM provider
- **Environment Isolation**: Index prefixing for multi-environment deployments

[Unreleased]: https://github.com/Knowledge-Innovation-Centre/doc-processor/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/Knowledge-Innovation-Centre/doc-processor/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Knowledge-Innovation-Centre/doc-processor/releases/tag/v1.0.0
