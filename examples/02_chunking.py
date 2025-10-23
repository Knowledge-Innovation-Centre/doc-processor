"""
Example 02: Advanced Chunking with docprocessor

This example demonstrates:
- Custom chunk sizes and overlap
- Different chunking strategies
- Token counting and optimization
- Handling various document types
"""

from pathlib import Path
from docprocessor import DocumentProcessor


def example_custom_chunk_sizes():
    """Demonstrate different chunk size configurations."""
    print("=" * 60)
    print("Example 1: Custom Chunk Sizes")
    print("=" * 60)

    # Small chunks for fine-grained search
    small_processor = DocumentProcessor(
        chunk_size=256,      # Small chunks
        chunk_overlap=25,    # Minimal overlap
        min_chunk_size=50    # Allow smaller chunks
    )

    # Large chunks for context preservation
    large_processor = DocumentProcessor(
        chunk_size=2048,     # Large chunks
        chunk_overlap=200,   # More overlap
        min_chunk_size=500   # Enforce minimum size
    )

    # Example text
    sample_text = """
    Artificial Intelligence has revolutionized many industries.
    Machine learning models can now process vast amounts of data.
    Deep learning networks have achieved remarkable accuracy.
    Natural language processing enables human-computer interaction.
    Computer vision systems can recognize objects and faces.
    """ * 10  # Repeat to create longer text

    # Create a temporary file
    temp_file = Path("temp_document.txt")
    temp_file.write_text(sample_text)

    try:
        # Process with small chunks
        small_result = small_processor.process(
            file_path=temp_file,
            extract_text=True,
            chunk=True
        )

        print(f"\nSmall chunks (256 tokens):")
        print(f"  Total chunks: {len(small_result.chunks)}")
        print(f"  Average tokens: {sum(c.token_count for c in small_result.chunks) / len(small_result.chunks):.0f}")
        print(f"  First chunk preview: {small_result.chunks[0].chunk_text[:100]}...")

        # Process with large chunks
        large_result = large_processor.process(
            file_path=temp_file,
            extract_text=True,
            chunk=True
        )

        print(f"\nLarge chunks (2048 tokens):")
        print(f"  Total chunks: {len(large_result.chunks)}")
        print(f"  Average tokens: {sum(c.token_count for c in large_result.chunks) / len(large_result.chunks):.0f}")
        print(f"  First chunk preview: {large_result.chunks[0].chunk_text[:100]}...")

    finally:
        # Clean up
        temp_file.unlink()


def example_chunk_overlap():
    """Demonstrate the effect of chunk overlap."""
    print("\n" + "=" * 60)
    print("Example 2: Chunk Overlap Impact")
    print("=" * 60)

    sample_text = "This is sentence one. This is sentence two. This is sentence three. " * 20

    # No overlap
    no_overlap = DocumentProcessor(chunk_size=200, chunk_overlap=0)

    # High overlap
    high_overlap = DocumentProcessor(chunk_size=200, chunk_overlap=100)

    no_overlap_chunks = no_overlap.chunk_text(text=sample_text, filename="test.txt")
    high_overlap_chunks = high_overlap.chunk_text(text=sample_text, filename="test.txt")

    print(f"\nNo overlap (0 tokens):")
    print(f"  Total chunks: {len(no_overlap_chunks)}")

    print(f"\nHigh overlap (100 tokens):")
    print(f"  Total chunks: {len(high_overlap_chunks)}")

    # Check for overlapping content
    if len(high_overlap_chunks) >= 2:
        chunk1_end = high_overlap_chunks[0].chunk_text[-50:]
        chunk2_start = high_overlap_chunks[1].chunk_text[:50]
        print(f"\n  Chunk 1 ends with: ...{chunk1_end}")
        print(f"  Chunk 2 starts with: {chunk2_start}...")
        print(f"  (Notice the overlapping content for better context)")


def example_different_file_types():
    """Demonstrate chunking different file formats."""
    print("\n" + "=" * 60)
    print("Example 3: Different File Types")
    print("=" * 60)

    processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)

    # Example 1: Plain text
    txt_file = Path("example.txt")
    txt_file.write_text("This is plain text content. " * 100)

    # Example 2: Markdown
    md_file = Path("example.md")
    md_file.write_text("""
# Heading 1
This is markdown content.

## Heading 2
- Bullet point 1
- Bullet point 2

Paragraph text here.
""" * 10)

    try:
        # Process TXT
        txt_result = processor.process(txt_file, extract_text=True, chunk=True)
        print(f"\nPlain Text (.txt):")
        print(f"  Chunks: {len(txt_result.chunks)}")
        print(f"  Format: {txt_result.metadata.get('format')}")

        # Process Markdown
        md_result = processor.process(md_file, extract_text=True, chunk=True)
        print(f"\nMarkdown (.md):")
        print(f"  Chunks: {len(md_result.chunks)}")
        print(f"  Format: {md_result.metadata.get('format')}")

    finally:
        txt_file.unlink()
        md_file.unlink()


def example_chunk_metadata():
    """Demonstrate chunk metadata and tracking."""
    print("\n" + "=" * 60)
    print("Example 4: Chunk Metadata")
    print("=" * 60)

    processor = DocumentProcessor()

    sample_text = "This is a test document for chunking. " * 50

    chunks = processor.chunk_text(
        text=sample_text,
        file_id="doc-12345",
        output_id="output-67890",
        project_id=42,
        filename="important_doc.txt",
        metadata={"author": "John Doe", "department": "Research"}
    )

    print(f"\nTotal chunks created: {len(chunks)}")
    print(f"\nFirst chunk details:")
    chunk = chunks[0]
    print(f"  Chunk ID: {chunk.chunk_id}")
    print(f"  File ID: {chunk.file_id}")
    print(f"  Output ID: {chunk.output_id}")
    print(f"  Project ID: {chunk.project_id}")
    print(f"  Filename: {chunk.filename}")
    print(f"  Chunk number: {chunk.chunk_number} of {chunk.total_chunks}")
    print(f"  Token count: {chunk.token_count}")
    print(f"  Metadata: {chunk.metadata}")
    print(f"  Text preview: {chunk.chunk_text[:100]}...")


def example_optimal_chunk_size():
    """Guide for choosing optimal chunk size."""
    print("\n" + "=" * 60)
    print("Example 5: Choosing Optimal Chunk Size")
    print("=" * 60)

    print("""
Chunk Size Guidelines:

1. For Semantic Search (Embedding-based):
   - Chunk size: 256-512 tokens
   - Overlap: 50-100 tokens
   - Why: Embeddings work best with focused, coherent text

2. For RAG (Retrieval Augmented Generation):
   - Chunk size: 512-1024 tokens
   - Overlap: 100-150 tokens
   - Why: LLMs need sufficient context to generate good responses

3. For Document Summarization:
   - Chunk size: 1024-2048 tokens
   - Overlap: 150-200 tokens
   - Why: Larger chunks preserve document structure

4. For Q&A Systems:
   - Chunk size: 256-512 tokens
   - Overlap: 50-100 tokens
   - Why: Questions typically relate to specific topics

5. For Code Documentation:
   - Chunk size: 128-256 tokens
   - Overlap: 25-50 tokens
   - Why: Code snippets are usually short and focused

Factors to Consider:
- Document type (technical vs. narrative)
- Target use case (search vs. generation)
- Available compute resources
- Storage constraints
- Query patterns
""")


def main():
    """Run all chunking examples."""
    print("\n" + "=" * 60)
    print("DOCPROCESSOR - ADVANCED CHUNKING EXAMPLES")
    print("=" * 60)

    try:
        example_custom_chunk_sizes()
        example_chunk_overlap()
        example_different_file_types()
        example_chunk_metadata()
        example_optimal_chunk_size()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        raise


if __name__ == "__main__":
    main()
