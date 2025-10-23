"""
Example 03: LLM Summarization with docprocessor

This example demonstrates:
- Integrating with different LLM providers
- Custom LLM client implementation
- Fallback summarization strategies
- Error handling and retries
"""

import os
from pathlib import Path
from docprocessor import DocumentProcessor


class OpenAIClient:
    """Example LLM client for OpenAI."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize OpenAI client."""
        self.api_key = api_key
        self.model = model

        # Import here to make it optional
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            print("Warning: openai package not installed. Install with: pip install openai")
            self.client = None

    def complete_chat(self, messages: list, temperature: float = 0.3) -> dict:
        """Complete chat using OpenAI API."""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000
            )

            return {"content": response.choices[0].message.content}

        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")


class AnthropicClient:
    """Example LLM client for Anthropic Claude."""

    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        """Initialize Anthropic client."""
        self.api_key = api_key
        self.model = model

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            print("Warning: anthropic package not installed. Install with: pip install anthropic")
            self.client = None

    def complete_chat(self, messages: list, temperature: float = 0.3) -> dict:
        """Complete chat using Anthropic API."""
        if not self.client:
            raise RuntimeError("Anthropic client not initialized")

        try:
            # Convert messages format
            system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
            user_messages = [m for m in messages if m["role"] != "system"]

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=temperature,
                system=system_msg,
                messages=user_messages
            )

            return {"content": response.content[0].text}

        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {e}")


class MockLLMClient:
    """Mock LLM client for testing without API keys."""

    def complete_chat(self, messages: list, temperature: float = 0.3) -> dict:
        """Return mock summary."""
        return {
            "content": "This is a mock summary. The document discusses important topics "
                       "and provides valuable insights. Key points include various aspects "
                       "of the subject matter, with detailed explanations and examples."
        }


def example_basic_summarization():
    """Demonstrate basic summarization with mock client."""
    print("=" * 60)
    print("Example 1: Basic Summarization")
    print("=" * 60)

    # Use mock client (no API key required)
    llm_client = MockLLMClient()

    processor = DocumentProcessor(
        llm_client=llm_client,
        summary_target_words=100
    )

    # Create sample document
    sample_text = """
    Machine Learning in Healthcare

    Machine learning is revolutionizing healthcare by enabling earlier disease
    detection, personalized treatment plans, and improved patient outcomes.

    Applications include:
    - Medical image analysis for detecting cancer and other diseases
    - Predictive analytics for patient risk assessment
    - Drug discovery and development acceleration
    - Electronic health record analysis for clinical insights

    The technology uses algorithms to analyze vast amounts of medical data,
    identifying patterns that humans might miss. Deep learning models can now
    match or exceed human performance in certain diagnostic tasks.

    Challenges remain, including data privacy concerns, algorithmic bias, and
    the need for regulatory frameworks. However, the potential benefits for
    patient care are immense.
    """ * 5

    temp_file = Path("healthcare_ml.txt")
    temp_file.write_text(sample_text)

    try:
        result = processor.process(
            file_path=temp_file,
            extract_text=True,
            chunk=True,
            summarize=True
        )

        print(f"\nOriginal document: {len(result.text)} characters")
        print(f"Generated summary: {len(result.summary)} characters")
        print(f"\nSummary:")
        print("-" * 60)
        print(result.summary)
        print("-" * 60)

    finally:
        temp_file.unlink()


def example_openai_summarization():
    """Demonstrate summarization with OpenAI."""
    print("\n" + "=" * 60)
    print("Example 2: OpenAI Summarization")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("\nSkipping: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return

    try:
        llm_client = OpenAIClient(api_key=api_key)

        processor = DocumentProcessor(
            llm_client=llm_client,
            summary_target_words=150,
            llm_temperature=0.5
        )

        sample_text = """
        Climate change is one of the most pressing challenges facing humanity.
        Rising global temperatures are causing sea levels to rise, extreme
        weather events to become more frequent, and ecosystems to be disrupted.
        """ * 10

        summary = processor.summarize_text(
            text=sample_text,
            filename="climate_change.txt"
        )

        print(f"\nOpenAI Summary:")
        print("-" * 60)
        print(summary)
        print("-" * 60)

    except Exception as e:
        print(f"\nError: {e}")


def example_anthropic_summarization():
    """Demonstrate summarization with Anthropic Claude."""
    print("\n" + "=" * 60)
    print("Example 3: Anthropic Claude Summarization")
    print("=" * 60)

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("\nSkipping: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key'")
        return

    try:
        llm_client = AnthropicClient(api_key=api_key)

        processor = DocumentProcessor(
            llm_client=llm_client,
            summary_target_words=200
        )

        sample_text = """
        Quantum computing represents a paradigm shift in computation.
        Unlike classical computers that use bits, quantum computers use
        quantum bits or qubits, which can exist in superposition states.
        """ * 10

        summary = processor.summarize_text(
            text=sample_text,
            filename="quantum_computing.txt"
        )

        print(f"\nAnthropic Summary:")
        print("-" * 60)
        print(summary)
        print("-" * 60)

    except Exception as e:
        print(f"\nError: {e}")


def example_fallback_summarization():
    """Demonstrate fallback summarization when LLM unavailable."""
    print("\n" + "=" * 60)
    print("Example 4: Fallback Summarization")
    print("=" * 60)

    # Create processor without LLM client
    processor = DocumentProcessor()

    sample_text = """
    Renewable energy sources are becoming increasingly important.
    Solar, wind, and hydroelectric power offer clean alternatives to
    fossil fuels. Investment in renewable infrastructure is growing
    rapidly as costs decline and efficiency improves.
    """ * 20

    # This will use fallback (simple truncation)
    summary = processor.summarize_text(
        text=sample_text,
        filename="renewable_energy.txt",
        use_fallback=True
    )

    print(f"\nFallback Summary (no LLM):")
    print("-" * 60)
    print(summary)
    print("-" * 60)
    print("\nNote: Fallback simply truncates text to target word count.")
    print("For better summaries, provide an LLM client.")


def example_custom_summary_length():
    """Demonstrate different summary lengths."""
    print("\n" + "=" * 60)
    print("Example 5: Custom Summary Lengths")
    print("=" * 60)

    llm_client = MockLLMClient()

    sample_text = "Artificial intelligence is transforming industries. " * 50

    # Short summary
    short_processor = DocumentProcessor(
        llm_client=llm_client,
        summary_target_words=50
    )

    # Long summary
    long_processor = DocumentProcessor(
        llm_client=llm_client,
        summary_target_words=500
    )

    short_summary = short_processor.summarize_text(sample_text, "ai.txt")
    long_summary = long_processor.summarize_text(sample_text, "ai.txt")

    print(f"\nShort summary (50 words target):")
    print(f"Length: {len(short_summary.split())} words")
    print(short_summary)

    print(f"\nLong summary (500 words target):")
    print(f"Length: {len(long_summary.split())} words")
    print(long_summary[:200] + "...")


def example_error_handling():
    """Demonstrate error handling in summarization."""
    print("\n" + "=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)

    class FailingLLMClient:
        """LLM client that always fails."""

        def complete_chat(self, messages, temperature):
            raise RuntimeError("API rate limit exceeded")

    processor = DocumentProcessor(llm_client=FailingLLMClient())

    sample_text = "Test document content. " * 20

    print("\nAttempting summarization with failing client...")

    try:
        # This will fail
        summary = processor.summarize_text(
            text=sample_text,
            filename="test.txt",
            use_fallback=False
        )
    except Exception as e:
        print(f"Expected error caught: {e}")

    print("\nUsing fallback on error...")

    # This will use fallback
    summary = processor.summarize_text(
        text=sample_text,
        filename="test.txt",
        use_fallback=True
    )

    print(f"Fallback summary generated: {len(summary)} characters")


def main():
    """Run all summarization examples."""
    print("\n" + "=" * 60)
    print("DOCPROCESSOR - LLM SUMMARIZATION EXAMPLES")
    print("=" * 60)

    try:
        example_basic_summarization()
        example_fallback_summarization()
        example_custom_summary_length()
        example_error_handling()

        # These require API keys
        example_openai_summarization()
        example_anthropic_summarization()

        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        raise


if __name__ == "__main__":
    main()
