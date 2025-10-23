#!/usr/bin/env python3
"""
Basic usage example for DocProcessor.

This example demonstrates:
1. Processing a document to extract text
2. Chunking the text into semantic segments
3. Optionally generating a summary (requires LLM)
"""

from pathlib import Path

from docprocessor import DocumentProcessor


def main():
    # Initialize processor
    print("Initializing Document Processor...")
    processor = DocumentProcessor(chunk_size=512, chunk_overlap=50, min_chunk_size=100)

    # Example 1: Extract text from a document
    print("\n--- Example 1: Extract Text Only ---")
    try:
        # Replace with your actual file path
        file_path = "sample.pdf"

        extraction = processor.extract_text(file_path)

        print(f"File: {file_path}")
        print(f"Extracted text length: {len(extraction['text'])} characters")
        print(f"Page count: {extraction['page_count']}")
        print(f"Format: {extraction['metadata'].get('format', 'unknown')}")
        print(f"First 200 chars: {extraction['text'][:200]}...")

    except Exception as e:
        print(f"Error: {e}")
        print("Note: Replace 'sample.pdf' with an actual file path")

    # Example 2: Full processing with chunking
    print("\n--- Example 2: Full Processing with Chunking ---")
    try:
        # Create a sample text file for testing
        sample_text = (
            """
        This is a sample document about artificial intelligence.

        Artificial intelligence (AI) is intelligence demonstrated by machines,
        in contrast to the natural intelligence displayed by humans and animals.
        Leading AI textbooks define the field as the study of intelligent agents.

        Machine learning is a subset of artificial intelligence that gives
        systems the ability to automatically learn and improve from experience
        without being explicitly programmed.

        Deep learning is part of a broader family of machine learning methods
        based on artificial neural networks with representation learning.
        """
            * 10
        )  # Repeat to make it long enough for chunking

        sample_file = Path("sample_text.txt")
        sample_file.write_text(sample_text)

        # Process with chunking
        result = processor.process(
            file_path=sample_file,
            extract_text=True,
            chunk=True,
            summarize=False,  # Set to True if you have an LLM client
        )

        print(f"File: {sample_file}")
        print(f"Extracted: {len(result.text)} characters")
        print(f"Created: {len(result.chunks)} chunks")

        # Show first chunk details
        if result.chunks:
            first_chunk = result.chunks[0]
            print(f"\nFirst Chunk:")
            print(f"  - ID: {first_chunk.chunk_id}")
            print(f"  - Number: {first_chunk.chunk_number + 1} of {first_chunk.total_chunks}")
            print(f"  - Tokens: {first_chunk.token_count}")
            print(f"  - Text preview: {first_chunk.chunk_text[:150]}...")

        # Cleanup
        sample_file.unlink()

    except Exception as e:
        print(f"Error: {e}")

    # Example 3: Converting chunks for search indexing
    print("\n--- Example 3: Prepare for Search Indexing ---")
    if result.chunks:
        search_docs = processor.chunks_to_search_documents(result.chunks)

        print(f"Converted {len(search_docs)} chunks to search document format")
        print(f"\nFirst search document keys: {list(search_docs[0].keys())}")
        print(f"Preview field: {search_docs[0]['chunk_preview'][:100]}...")


if __name__ == "__main__":
    main()
