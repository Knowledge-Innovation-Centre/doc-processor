#!/bin/bash
set -e

echo "🚀 Setting up docprocessor development environment..."

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install system dependencies for document processing
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install package in editable mode with dev dependencies
echo "📚 Installing docprocessor with dev dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
if [ -f ".pre-commit-config.yaml" ]; then
    pip install pre-commit
    pre-commit install
    echo "✅ Pre-commit hooks installed"
else
    echo "⚠️ No .pre-commit-config.yaml found, skipping pre-commit setup"
fi

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
if pytest --version > /dev/null 2>&1; then
    pytest tests/ -v || echo "⚠️ Some tests failed, but setup is complete"
else
    echo "⚠️ pytest not found, skipping test verification"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  • Run tests: pytest"
echo "  • Run tests with coverage: pytest --cov=docprocessor"
echo "  • Format code: black docprocessor tests"
echo "  • Sort imports: isort docprocessor tests"
echo "  • Type check: mypy docprocessor"
echo ""
