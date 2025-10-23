"""
Example 05: Custom LLM Client Implementation

This example demonstrates:
- Building custom LLM clients for different providers
- Implementing error handling and retries
- Supporting multiple providers
- Best practices for LLM integration
"""

import time
from typing import Any, Dict, List

from docprocessor import DocumentProcessor


class RetryableLLMClient:
    """
    LLM client with automatic retry logic.

    Implements exponential backoff for handling rate limits and transient errors.
    """

    def __init__(self, base_client, max_retries: int = 3, base_delay: float = 1.0):
        """
        Initialize retryable client.

        Args:
            base_client: Underlying LLM client
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds for exponential backoff
        """
        self.base_client = base_client
        self.max_retries = max_retries
        self.base_delay = base_delay

    def complete_chat(self, messages: List[Dict], temperature: float = 0.3) -> Dict[str, Any]:
        """Complete chat with retry logic."""
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return self.base_client.complete_chat(messages, temperature)

            except Exception as e:
                last_error = e
                error_msg = str(e).lower()

                # Check if error is retryable
                if any(keyword in error_msg for keyword in ["rate limit", "timeout", "overloaded"]):
                    if attempt < self.max_retries - 1:
                        # Exponential backoff
                        delay = self.base_delay * (2**attempt)
                        print(f"Retry attempt {attempt + 1}/{self.max_retries} after {delay}s...")
                        time.sleep(delay)
                        continue

                # Non-retryable error or max retries exceeded
                raise

        # All retries exhausted
        raise RuntimeError(f"Failed after {self.max_retries} attempts: {last_error}")


class MultiProviderLLMClient:
    """
    LLM client that supports multiple providers with fallback.

    Tries providers in order until one succeeds.
    """

    def __init__(self, providers: List[Any]):
        """
        Initialize multi-provider client.

        Args:
            providers: List of LLM client instances in priority order
        """
        if not providers:
            raise ValueError("At least one provider required")

        self.providers = providers

    def complete_chat(self, messages: List[Dict], temperature: float = 0.3) -> Dict[str, Any]:
        """Try each provider in order until one succeeds."""
        errors = []

        for i, provider in enumerate(self.providers):
            try:
                print(f"Attempting provider {i + 1}/{len(self.providers)}...")
                return provider.complete_chat(messages, temperature)

            except Exception as e:
                errors.append((provider.__class__.__name__, str(e)))
                if i < len(self.providers) - 1:
                    print(f"  Failed: {e}. Trying next provider...")
                    continue

        # All providers failed
        error_summary = "\n".join([f"  - {name}: {err}" for name, err in errors])
        raise RuntimeError(f"All providers failed:\n{error_summary}")


class CachingLLMClient:
    """
    LLM client with response caching.

    Caches responses based on message content to avoid redundant API calls.
    """

    def __init__(self, base_client):
        """Initialize caching client."""
        self.base_client = base_client
        self.cache: Dict[str, Dict[str, Any]] = {}

    def _get_cache_key(self, messages: List[Dict], temperature: float) -> str:
        """Generate cache key from messages and temperature."""
        import hashlib
        import json

        content = json.dumps({"messages": messages, "temperature": temperature}, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def complete_chat(self, messages: List[Dict], temperature: float = 0.3) -> Dict[str, Any]:
        """Complete chat with caching."""
        cache_key = self._get_cache_key(messages, temperature)

        # Check cache
        if cache_key in self.cache:
            print("  (using cached response)")
            return self.cache[cache_key]

        # Call API
        response = self.base_client.complete_chat(messages, temperature)

        # Cache response
        self.cache[cache_key] = response

        return response

    def clear_cache(self):
        """Clear the response cache."""
        self.cache.clear()

    def cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {"cached_responses": len(self.cache)}


class TokenCountingLLMClient:
    """
    LLM client that tracks token usage.

    Useful for monitoring API costs and usage patterns.
    """

    def __init__(self, base_client):
        """Initialize token counting client."""
        self.base_client = base_client
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.request_count = 0

    def _estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count (4 chars ≈ 1 token)."""
        return len(text) // 4

    def complete_chat(self, messages: List[Dict], temperature: float = 0.3) -> Dict[str, Any]:
        """Complete chat with token tracking."""
        # Estimate input tokens
        input_text = " ".join([m.get("content", "") for m in messages])
        input_tokens = self._estimate_tokens(input_text)

        # Call API
        response = self.base_client.complete_chat(messages, temperature)

        # Estimate output tokens
        output_text = response.get("content", "")
        output_tokens = self._estimate_tokens(output_text)

        # Update statistics
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.request_count += 1

        print(f"  Tokens: {input_tokens} in, {output_tokens} out")

        return response

    def usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "total_requests": self.request_count,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "avg_input_tokens": self.total_input_tokens / max(self.request_count, 1),
            "avg_output_tokens": self.total_output_tokens / max(self.request_count, 1),
        }


class MockLLMClient:
    """Simple mock LLM client for examples."""

    def complete_chat(self, messages: List[Dict], temperature: float = 0.3) -> Dict[str, Any]:
        """Return mock response."""
        return {"content": "This is a mock LLM response summarizing the document content."}


def example_retry_logic():
    """Demonstrate retry logic with LLM client."""
    print("=" * 60)
    print("Example 1: Retry Logic")
    print("=" * 60)

    # Create flaky client (fails sometimes)
    class FlakyClient:
        def __init__(self):
            self.attempts = 0

        def complete_chat(self, messages, temperature):
            self.attempts += 1
            if self.attempts < 2:
                raise RuntimeError("Rate limit exceeded (simulated)")
            return {"content": "Success after retry!"}

    base_client = FlakyClient()
    retryable_client = RetryableLLMClient(base_client, max_retries=3)

    processor = DocumentProcessor(llm_client=retryable_client)

    sample_text = "Test document for retry logic. " * 20

    try:
        summary = processor.summarize_text(sample_text, "test.txt")
        print(f"\nSuccessfully generated summary after retries!")
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"\nFailed: {e}")


def example_multi_provider():
    """Demonstrate multi-provider fallback."""
    print("\n" + "=" * 60)
    print("Example 2: Multi-Provider Fallback")
    print("=" * 60)

    class FailingProvider:
        def complete_chat(self, messages, temperature):
            raise RuntimeError("Provider unavailable")

    class WorkingProvider:
        def complete_chat(self, messages, temperature):
            return {"content": "Fallback provider succeeded!"}

    # Try failing provider first, then fallback to working one
    multi_provider = MultiProviderLLMClient([FailingProvider(), WorkingProvider()])

    processor = DocumentProcessor(llm_client=multi_provider)

    sample_text = "Test document for fallback. " * 20

    summary = processor.summarize_text(sample_text, "test.txt")
    print(f"\nGenerated summary using fallback provider:")
    print(f"Summary: {summary}")


def example_caching():
    """Demonstrate response caching."""
    print("\n" + "=" * 60)
    print("Example 3: Response Caching")
    print("=" * 60)

    base_client = MockLLMClient()
    caching_client = CachingLLMClient(base_client)

    processor = DocumentProcessor(llm_client=caching_client)

    sample_text = "Test document for caching. " * 20

    # First call - will hit API
    print("\nFirst summarization (API call):")
    summary1 = processor.summarize_text(sample_text, "test.txt")

    # Second call - will use cache
    print("\nSecond summarization (same text):")
    summary2 = processor.summarize_text(sample_text, "test.txt")

    print(f"\nSummaries match: {summary1 == summary2}")
    print(f"Cache stats: {caching_client.cache_stats()}")


def example_token_tracking():
    """Demonstrate token usage tracking."""
    print("\n" + "=" * 60)
    print("Example 4: Token Usage Tracking")
    print("=" * 60)

    base_client = MockLLMClient()
    tracking_client = TokenCountingLLMClient(base_client)

    processor = DocumentProcessor(llm_client=tracking_client)

    # Process multiple documents
    documents = [
        "Short document. " * 10,
        "Medium document. " * 50,
        "Long document. " * 200,
    ]

    for i, text in enumerate(documents, 1):
        print(f"\nProcessing document {i}:")
        processor.summarize_text(text, f"doc{i}.txt")

    # Print usage statistics
    stats = tracking_client.usage_stats()
    print(f"\n{'=' * 60}")
    print("Usage Statistics:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Total tokens: {stats['total_tokens']:,}")
    print(f"  Input tokens: {stats['total_input_tokens']:,}")
    print(f"  Output tokens: {stats['total_output_tokens']:,}")
    print(f"  Avg input tokens/request: {stats['avg_input_tokens']:.0f}")
    print(f"  Avg output tokens/request: {stats['avg_output_tokens']:.0f}")


def example_combined_features():
    """Demonstrate combining multiple features."""
    print("\n" + "=" * 60)
    print("Example 5: Combined Features")
    print("=" * 60)

    # Stack multiple wrappers
    base_client = MockLLMClient()

    # Add caching
    client_with_cache = CachingLLMClient(base_client)

    # Add token tracking
    client_with_tracking = TokenCountingLLMClient(client_with_cache)

    # Add retry logic
    robust_client = RetryableLLMClient(client_with_tracking)

    processor = DocumentProcessor(llm_client=robust_client)

    print("\nClient stack:")
    print("  1. Base LLM client")
    print("  2. + Caching")
    print("  3. + Token tracking")
    print("  4. + Retry logic")

    sample_text = "Test document with combined features. " * 20

    print("\nFirst call:")
    summary1 = processor.summarize_text(sample_text, "test.txt")

    print("\nSecond call (will use cache):")
    summary2 = processor.summarize_text(sample_text, "test.txt")

    print(f"\nCache hit: {summary1 == summary2}")


def main():
    """Run all custom LLM client examples."""
    print("\n" + "=" * 60)
    print("DOCPROCESSOR - CUSTOM LLM CLIENT EXAMPLES")
    print("=" * 60)

    try:
        example_retry_logic()
        example_multi_provider()
        example_caching()
        example_token_tracking()
        example_combined_features()

        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        raise


if __name__ == "__main__":
    main()
