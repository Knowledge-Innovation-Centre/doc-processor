# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Devcontainer configuration for GitHub Codespaces and VS Code Remote Containers
- Modern Python packaging with `pyproject.toml`
- Pre-commit hooks for code quality (Black, isort, flake8, mypy)
- GitHub Actions CI/CD pipeline
- Comprehensive test configuration with coverage reporting
- CONTRIBUTING.md with contribution guidelines
- This CHANGELOG.md file

### Changed
- Enhanced README.md with better documentation
- Improved project structure and organization

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
- Comprehensive test suite (66 tests across 3 test files)
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

[Unreleased]: https://github.com/Knowledge-Innovation-Centre/doc-processor/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Knowledge-Innovation-Centre/doc-processor/releases/tag/v1.0.0
