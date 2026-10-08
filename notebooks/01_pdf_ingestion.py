# Databricks notebook source
# MAGIC %md
# MAGIC # Lesson 1 — SageMaker PDF ingestion and chunking
# MAGIC
# MAGIC **Goal:** Load 3 AWS SageMaker documentation PDFs from a Unity Catalog
# MAGIC volume, extract page text, create reproducible chunks and save Delta rows.
# MAGIC
# MAGIC **Prerequisites:** Upload deployment_options.pdf, async_inference.pdf
# MAGIC and serverless_inference.pdf to your volume (see README). Set CATALOG
# MAGIC below to a catalog where you can create a schema and volume.

# COMMAND ----------
# MAGIC %pip install 'pymupdf>=1.24,<2'

# COMMAND ----------
from pathlib import Path
import sys

# In a Databricks Git folder, notebooks run with their containing folder as
# the current working directory. Add the repository root to import src/.
PROJECT_ROOT = Path.cwd().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion import extract_pdf_pages, chunk_pages

CATALOG = "main"  # Change if your workspace uses another writable catalog
SCHEMA = "rag_lab"
VOLUME = "sagemaker_pdfs"
TABLE = "document_chunks"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {chr(96)}{CATALOG}{chr(96)}.{chr(96)}{SCHEMA}{chr(96)}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {chr(96)}{CATALOG}{chr(96)}.{chr(96)}{SCHEMA}{chr(96)}.{chr(96)}{VOLUME}{chr(96)}")

pdf_folder = Path(f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}")
print("Upload PDFs to:", pdf_folder)

# COMMAND ----------
pdf_files = sorted(pdf_folder.glob("*.pdf"))
print("PDF files:", [p.name for p in pdf_files])

expected = {"deployment_options.pdf", "async_inference.pdf", "serverless_inference.pdf"}
found = {p.name for p in pdf_files}
assert expected.issubset(found), f"Missing PDFs: {sorted(expected - found)}"

pages = []
for pdf_file in pdf_files:
    pages.extend(extract_pdf_pages(pdf_file))

print("Pages extracted:", len(pages))
assert pages, "No text could be extracted. PDFs may be scanned/image-based."
print("Sample:", pages[0]["text"][:350])

# COMMAND ----------
chunks = chunk_pages(pages, chunk_size=200, chunk_overlap=40)
assert chunks, "No chunks created"

print("Chunks:", len(chunks))
print("Sample chunk:", chunks[0])

# COMMAND ----------
df = spark.createDataFrame(chunks)
full_table_name = f"{chr(96)}{CATALOG}{chr(96)}.{chr(96)}{SCHEMA}{chr(96)}.{chr(96)}{TABLE}{chr(96)}"

# This overwrites the lab table each time for reproducible first-run experiments.
# Do not use this overwrite pattern for production append/change-data pipelines.
(df.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(full_table_name))

print("Saved Delta table:", full_table_name)
display(spark.table(full_table_name).limit(10))

# COMMAND ----------
summary = spark.sql(f"""
    SELECT document_name, COUNT(*) AS total_chunks,
           MIN(page_number) AS first_page, MAX(page_number) AS last_page
    FROM {full_table_name}
    GROUP BY document_name
    ORDER BY document_name
""")
display(summary)

# COMMAND ----------
keyword_matches = spark.sql(f"""
    SELECT document_name, page_number,
           LEFT(chunk_text, 350) AS matched_text
    FROM {full_table_name}
    WHERE LOWER(chunk_text) LIKE '%serverless%'
    LIMIT 5
""")
display(keyword_matches)

print("Lesson 1 successful: ingestion, chunking, Delta persistence, keyword sanity check.")
