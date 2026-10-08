# Progress journal

## Week 1 — PDF ingestion and chunking

**Problem:** A documentation assistant needs reliable, traceable source text.

**Implementation started:**
- Page-by-page PDF extraction using PyMuPDF.
- Overlapping word chunking with stable SHA-256 chunk IDs.
- Source URL, document name and page number metadata.
- Databricks notebook for Delta persistence and keyword sanity check.
- Unit tests for chunk boundaries, determinism and validation.

**Verified locally:** Python chunking unit tests.

**Still to verify in the Databricks workspace:**
- Upload the three PDFs and run all notebook cells.
- Capture actual row counts per source PDF.
- Inspect noisy headers, tables and poor-quality PDF text extraction.

**Engineering decision:** Start with 200-word chunks and 40-word overlap as
an experimental baseline, not an asserted optimum.

## Next steps

1. Index the Delta table using an embedding model and Databricks AI Search.
2. Compare keyword search with semantic retrieval.
3. Add grounded answer generation and source citations.
4. Evaluate on a stable question set before tuning.

When you complete a step, update this file and link to a commit or screenshot.
