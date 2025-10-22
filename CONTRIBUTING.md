# Contributing to docprocessor

We love your input! We want to make contributing to docprocessor as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Request Process

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the code style (use pre-commit hooks)
6. Issue that pull request!

## Development Setup

### Using GitHub Codespaces (Recommended)

The easiest way to contribute is using GitHub Codespaces:

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait for the devcontainer to build and install dependencies
3. Start coding!

All dependencies and tools are pre-configured.

### Local Development

#### Prerequisites
- Python 3.8+
- Tesseract OCR
- Poppler utils

#### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

**Windows:**
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/)

#### Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/doc-processor.git
cd doc-processor

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style

We use automated tools to maintain code quality:

- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Running Code Quality Checks

```bash
# Format code
black docprocessor tests

# Sort imports
isort docprocessor tests

# Lint
flake8 docprocessor tests

# Type check
mypy docprocessor
```

Or use pre-commit to run all checks:

```bash
pre-commit run --all-files
```

## Testing

We aim for >80% test coverage. Please add tests for any new features or bug fixes.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=docprocessor

# Run specific test file
pytest tests/test_processor.py -v

# Run specific test
pytest tests/test_processor.py::TestDocumentProcessor::test_process_pdf -v

# Run tests matching pattern
pytest -k "test_extract" -v

# Skip slow tests
pytest -m "not slow"
```

### Writing Tests

Tests are located in the `tests/` directory and use pytest.

Example test structure:

```python
import pytest
from docprocessor import DocumentProcessor

class TestDocumentProcessor:
    """Tests for DocumentProcessor class"""

    def test_process_pdf(self, tmp_path):
        """Test processing a PDF file"""
        # Arrange
        processor = DocumentProcessor()
        pdf_file = tmp_path / "test.pdf"
        # ... create test file

        # Act
        result = processor.process(pdf_file, extract_text=True)

        # Assert
        assert result.text
        assert result.page_count > 0
```

## Documentation

### Docstring Style

We use Google-style docstrings:

```python
def process(
    self,
    file_path: Union[str, Path],
    extract_text: bool = True,
    chunk: bool = False,
    summarize: bool = False,
    **metadata: Any
) -> ProcessResult:
    """Process a document through the full pipeline.

    Args:
        file_path: Path to the document file
        extract_text: Whether to extract text content
        chunk: Whether to chunk the document
        summarize: Whether to generate a summary (requires LLM client)
        **metadata: Additional metadata to attach to chunks

    Returns:
        ProcessResult containing text, chunks, summary, and metadata

    Raises:
        FileNotFoundError: If file_path does not exist
        ValueError: If summarize=True but no LLM client configured
        RuntimeError: If processing fails

    Examples:
        >>> processor = DocumentProcessor()
        >>> result = processor.process("document.pdf", chunk=True)
        >>> print(f"Created {len(result.chunks)} chunks")
    """
```

## Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:

```
Add support for Excel files

- Add ExcelExtractor class
- Update ContentExtractor to handle .xlsx files
- Add tests for Excel extraction
- Update documentation

Fixes #123
```

## Branching Strategy

- `main` - stable release branch
- `develop` - development branch (if used)
- `feature/*` - new features
- `bugfix/*` - bug fixes
- `hotfix/*` - urgent fixes for production

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Release Process

1. Update version in `docprocessor/__init__.py`
2. Update `CHANGELOG.md` with version and date
3. Commit changes: `git commit -m "Bump version to X.Y.Z"`
4. Create tag: `git tag vX.Y.Z`
5. Push: `git push origin main --tags`
6. GitHub Actions will automatically build and publish to PyPI

## Issue Reporting

### Bug Reports

Please include:

- Python version
- Operating system
- docprocessor version
- Minimal code to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages and stack traces

### Feature Requests

Please include:

- Use case description
- Proposed API (if applicable)
- Alternative approaches considered
- Willingness to contribute the implementation

## Code Review Process

All submissions require review. We use GitHub pull requests for this purpose.

Reviewers will check for:

- Code quality and style compliance
- Test coverage
- Documentation updates
- Backwards compatibility
- Performance implications

## Community Guidelines

- Be welcoming and inclusive
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

---

Thank you for contributing to docprocessor! 🎉
