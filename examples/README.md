# docprocessor Examples

This directory contains practical examples demonstrating various features and use cases of the docprocessor library.

## Examples Overview

### 01. Basic Usage (`basic_usage.py`)
- Simple document processing
- Text extraction and basic chunking
- Getting started with the library

### 02. Advanced Chunking (`02_chunking.py`)
- Custom chunk sizes and overlap
- Token-based chunking configuration
- Handling different document types

### 03. LLM Summarization (`03_summarization.py`)
- Integrating with LLM providers (OpenAI, Anthropic, etc.)
- Custom LLM client implementation
- Fallback summarization strategies

### 04. Meilisearch Integration (`04_meilisearch_integration.py`)
- Complete indexing pipeline
- Two-index architecture (chunks + documents)
- Searching and filtering results

### 05. Custom LLM Client (`05_custom_llm_client.py`)
- Building custom LLM clients
- Support for different providers
- Error handling and retries

### 06. Batch Processing (`06_batch_processing.py`)
- Processing multiple documents
- Parallel processing strategies
- Progress tracking and error handling

### 07. Multi-Environment Deployment (`07_multi_environment.py`)
- Environment-specific configurations
- Index prefixing for dev/staging/prod
- Configuration management

## Running the Examples

### Prerequisites

```bash
# Install docprocessor with all dependencies
pip install -e ".[dev]"

# Install system dependencies (if needed)
# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# macOS
brew install tesseract poppler
```

### Environment Variables

Some examples require environment variables:

```bash
# For LLM examples (choose your provider)
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# For Meilisearch examples
export MEILISEARCH_URL="http://localhost:7700"
export MEILISEARCH_API_KEY="your-master-key"
```

### Running an Example

```bash
# Navigate to examples directory
cd examples

# Run an example
python 01_basic_usage.py

# Or run directly
python -m examples.03_summarization
```

## Example Files

Each example is self-contained and includes:
- Clear comments explaining each step
- Error handling demonstrations
- Expected output examples
- Tips and best practices

## Sample Data

Some examples include or reference sample documents:
- `sample_data/` - Test documents for examples
- PDFs, DOCX, TXT files for testing

## Getting Help

- **Documentation**: See [README.md](../README.md)
- **API Reference**: Check docstrings in source code
- **Issues**: [GitHub Issues](https://github.com/Knowledge-Innovation-Centre/doc-processor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Knowledge-Innovation-Centre/doc-processor/discussions)

## Contributing Examples

Have a great use case? Contributions are welcome!

1. Create a new numbered example file
2. Include clear comments and documentation
3. Add entry to this README
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
