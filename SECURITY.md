# Security Policy

## Supported Versions

We actively support the following versions of docprocessor with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of docprocessor seriously. If you have discovered a security vulnerability, please report it to us privately.

### How to Report a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Email**: Send details to **security@knowledgeinnovation.eu**
2. **GitHub Security Advisories**: Use the [private vulnerability reporting feature](https://github.com/Knowledge-Innovation-Centre/doc-processor/security/advisories/new)

### What to Include

Please include as much of the following information as possible:

- Type of vulnerability (e.g., injection, XSS, authentication bypass, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- We will acknowledge receipt of your vulnerability report within **48 hours**
- We will send a more detailed response within **7 days** indicating the next steps
- We will keep you informed about the progress toward a fix
- We may ask for additional information or guidance during the process

### Disclosure Policy

- We request that you give us reasonable time to address the vulnerability before public disclosure
- We will credit you in the security advisory unless you prefer to remain anonymous
- Once a fix is available, we will:
  1. Release a patched version
  2. Publish a security advisory
  3. Credit the reporter (if permission granted)
  4. Update the CHANGELOG.md

## Security Best Practices

When using docprocessor, we recommend:

### Input Validation

- **Validate file paths**: Always validate and sanitize file paths from user input
- **Limit file sizes**: Set reasonable limits on document sizes to prevent DoS
- **File type verification**: Verify file types match expected formats

```python
from pathlib import Path

# Good: Validate file path
file_path = Path(user_input).resolve()
if not file_path.is_file():
    raise ValueError("Invalid file path")

# Good: Check file extension
allowed_extensions = {'.pdf', '.txt', '.docx', '.md'}
if file_path.suffix.lower() not in allowed_extensions:
    raise ValueError("Unsupported file type")
```

### LLM Client Security

- **API Key Protection**: Never commit API keys to version control
- **Use environment variables**: Store sensitive credentials in environment variables
- **Implement rate limiting**: Protect against abuse of LLM APIs

```python
import os

# Good: Use environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not configured")
```

### Meilisearch Security

- **Use strong API keys**: Generate secure random API keys
- **Network isolation**: Run Meilisearch behind a firewall
- **Enable authentication**: Always require authentication in production
- **Use HTTPS**: Encrypt data in transit

```python
# Good: Use environment-specific configuration
indexer = MeiliSearchIndexer(
    url=os.getenv("MEILISEARCH_URL"),
    api_key=os.getenv("MEILISEARCH_API_KEY"),
    index_prefix=os.getenv("ENV_PREFIX", "prod_")
)
```

### Document Processing

- **OCR limits**: Be aware that OCR processing can be resource-intensive
- **Temporary file cleanup**: Ensure temporary files are cleaned up
- **Memory management**: Monitor memory usage with large documents

```python
# Good: Use context managers for file handling
from pathlib import Path

def process_safely(file_path: Path):
    try:
        processor = DocumentProcessor()
        result = processor.process(file_path)
        return result
    finally:
        # Clean up any temporary files if needed
        pass
```

## Known Security Considerations

### Third-Party Dependencies

docprocessor depends on several third-party libraries. We:

- Regularly update dependencies to patch known vulnerabilities
- Use Dependabot to monitor for security updates
- Pin dependency versions in production deployments

### OCR and Image Processing

- **Malicious images**: Be cautious with user-uploaded images
- **Resource exhaustion**: Large images can consume significant memory
- **Tesseract vulnerabilities**: Keep Tesseract OCR updated

### PDF Processing

- **Malformed PDFs**: PDFs can contain malicious content
- **Embedded scripts**: Be aware of JavaScript in PDFs
- **File size attacks**: Extremely large PDFs can cause DoS

## Security Features

### Built-in Protections

- **File type validation**: Checks file extensions before processing
- **Error handling**: Proper exception handling prevents information leakage
- **Logging**: Security-relevant events are logged (without sensitive data)
- **Input sanitization**: File paths and parameters are validated

### What We Don't Do

For security and privacy reasons, docprocessor:

- Does NOT transmit your documents to external services (except your configured LLM)
- Does NOT store documents or API keys
- Does NOT log document content
- Does NOT include analytics or telemetry

## Security Updates

Security updates are released as soon as possible after a vulnerability is confirmed. Updates are published:

1. As patch releases (e.g., 1.0.1 → 1.0.2)
2. With a security advisory in GitHub
3. With a note in CHANGELOG.md
4. Via GitHub notifications to repository watchers

To receive security updates:

- Watch the repository on GitHub
- Subscribe to release notifications
- Follow [@KnowledgeInnov](https://twitter.com/KnowledgeInnov) (if available)

## Acknowledgments

We thank the following security researchers for responsibly disclosing vulnerabilities:

- _(None yet - be the first!)_

## Questions?

If you have questions about this security policy, please contact:

- **Email**: info@knowledgeinnovation.eu
- **GitHub Discussions**: [Security category](https://github.com/Knowledge-Innovation-Centre/doc-processor/discussions/categories/security)

---

**Last Updated**: 2025-10-22
**Version**: 1.0
