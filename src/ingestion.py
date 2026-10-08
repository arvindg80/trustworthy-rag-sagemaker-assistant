"""Deterministic, page-aware ingestion helpers for SageMaker documentation PDFs.

The pure chunking functions are intentionally usable outside Databricks to
make local unit testing easy.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Iterable


SOURCE_URLS = {
    "deployment_options.pdf": "https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-deployment.html",
    "async_inference.pdf": "https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html",
    "serverless_inference.pdf": "https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html",
}


def extract_pdf_pages(pdf_file: Path) -> list[dict]:
    """Extract nonempty pages while preserving filename and page number."""
    import fitz  # PyMuPDF - imported only when PDF processing is requested

    pages = []
    with fitz.open(str(pdf_file)) as doc:
        for page_number, page in enumerate(doc, start=1):
            content = page.get_text("text", sort=True).strip()
            if content:
                pages.append(
                    {
                        "document_name": pdf_file.name,
                        "page_number": page_number,
                        "text": content,
                    }
                )
    return pages


def chunk_pages(
    pages: Iterable[dict],
    chunk_size: int = 200,
    chunk_overlap: int = 40,
    source_urls: dict[str, str] | None = None,
) -> list[dict]:
    """Split individual pages into overlapping word chunks.

    These are *word* counts, not model tokens. An improved token- and
    heading-aware strategy is planned for later experiments.
    """
    if chunk_size <= 0 or not (0 <= chunk_overlap < chunk_size):
        raise ValueError("Require chunk_size > 0 and 0 <= chunk_overlap < chunk_size")

    urls = source_urls if source_urls is not None else SOURCE_URLS
    result = []
    step = chunk_size - chunk_overlap

    for page in pages:
        words = page["text"].split()
        # Stop after the first chunk that reaches the page end; this avoids
        # redundant final chunks consisting entirely of overlap words.
        for start in range(0, len(words), step):
            chunk_words = words[start : start + chunk_size]
            if not chunk_words:
                break

            content = " ".join(chunk_words)
            doc_name = page["document_name"]
            page_number = int(page["page_number"])
            unique_text = f"{doc_name}|{page_number}|{start}|{content}"
            chunk_id = sha256(unique_text.encode("utf-8")).hexdigest()

            result.append(
                {
                    "chunk_id": chunk_id,
                    "document_name": doc_name,
                    "page_number": page_number,
                    "chunk_text": content,
                    "source_url": urls.get(doc_name, ""),
                }
            )
            if start + chunk_size >= len(words):
                break
    return result
