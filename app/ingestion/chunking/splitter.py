import logfire
from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 1500,
    chunk_overlap: int = 200,
) -> List[str]:
    """
    Split text into chunks of approximately `chunk_size` characters.

    Strategy:
    1. First try to respect paragraph boundaries.
    2. If a paragraph is too large, split it into smaller chunks.
    3. Add overlap between chunks for better retrieval context.
    """

    with logfire.span(
        "✂️ Text Chunking",
        text_length=len(text),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    ):

        if not text or not text.strip():
            return []

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Split into paragraphs
        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:

            # -------------------------------------------------
            # Case 1: Paragraph itself is larger than chunk_size
            # -------------------------------------------------
            if len(paragraph) > chunk_size:

                # First save the current accumulated chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                # Split large paragraph into fixed-size pieces
                start = 0

                while start < len(paragraph):
                    end = start + chunk_size

                    piece = paragraph[start:end].strip()

                    if piece:
                        chunks.append(piece)

                    # Move back by overlap amount
                    start = end - chunk_overlap

                continue

            # -------------------------------------------------
            # Case 2: Add paragraph to current chunk
            # -------------------------------------------------
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:

                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph

            else:

                # Save current chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Start new chunk
                current_chunk = paragraph

        # -------------------------------------------------
        # Save remaining chunk
        # -------------------------------------------------
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Remove empty chunks
        valid_chunks = [
            chunk
            for chunk in chunks
            if chunk.strip()
        ]

        logfire.info(
            f"✅ Generated {len(valid_chunks)} chunks "
            f"from {len(text)} characters"
        )

        return valid_chunks