# Trustworthy RAG: Amazon SageMaker Documentation Assistant

> **Status:** Week 1 — PDF ingestion and chunking starter. Search, LLM orchestration,
> and RAG evaluation are planned, **not yet implemented**.

A public build-in-the-open AI engineering project inspired by the Sundog
Education community's **Challenge #1: Amazon SageMaker Documentation Assistant**.

## The problem

Amazon SageMaker AI documentation is extensive and evolving. Engineers need
accurate, source-grounded answers instead of persuasive but unverified responses.
We are building a retrieval-augmented assistant and measuring its quality
rather than assuming that plausible text is correct.

## Target architecture

~~~text
AWS SageMaker documentation PDFs
    -> PyMuPDF (extract text by page)
    -> Word chunks + metadata
    -> Unity Catalog Delta table
    -> [Planned: Databricks AI Search + embeddings]
    -> [Planned: Python RAG orchestration + LLM]
    -> [Planned: citation-based answers + UI]
    -> [Planned: MLflow tracing + Ragas evaluation]
~~~

## Run Lesson 1 on Azure Databricks

1. Create a Databricks **Git folder** connected to this repository.
2. Open **notebooks/01_pdf_ingestion.py** as a Databricks source notebook.
3. Attach supported compute. You need privileges to create a schema and volume
   in the chosen Unity Catalog catalog.
4. Set the CATALOG variable in the notebook (defaults to main).
5. Run the first setup cells. Upload the following PDFs via **Catalog Explorer**
   into /Volumes/<CATALOG>/rag_lab/sagemaker_pdfs/:
   - deployment_options.pdf — https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-deployment.html
   - async_inference.pdf — https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html
   - serverless_inference.pdf — https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html

   Start by opening the official pages and using the browser's **Print → Save as PDF**.
   These source documents aren't committed to this repository.
6. Continue running the notebook. It creates rag_lab.document_chunks
   and displays sanity-check results.

**Note:** The ingestion notebook currently overwrites the *lab* Delta table
on each run. Don't point it at a production table. This is a deliberately
simple proof-of-concept design.

## Test without Databricks

Python 3.10+:

~~~bash
python -m unittest discover -s tests -v
~~~

For actual PDF extraction outside Databricks, also install:

~~~bash
pip install -r requirements.txt
~~~

## Milestones

| Milestone | Status | Evidence |
|---|---|---|
| Repository scaffold and deterministic chunking tests | Implemented locally | tests/test_ingestion.py |
| PDF ingestion and Delta table | Code ready; workspace run pending | notebooks/01_pdf_ingestion.py |
| Embeddings and AI Search | Planned | — |
| Retrieval + cited LLM answers | Planned | — |
| Evaluation benchmark, Ragas, MLflow | Planned | — |
| Chunking/retrieval tuning and cost comparison | Planned | — |

Progress notes: [docs/PROGRESS.md](docs/PROGRESS.md).

## Tech choices

- **Python and PyMuPDF:** page-aware PDF text extraction.
- **Unity Catalog volumes:** file storage on Databricks.
- **Delta tables:** structured, inspectable chunks and metadata.
- **Planned:** Databricks AI Search, LLM, Ragas and MLflow.

## Security and documentation ownership

- Never commit PATs, API keys, .env files, credentials or internal data.
- PDFs and large datasets stay out of Git. Link to the original AWS documentation.
- This is an independent learning project and is not affiliated with AWS.
- Public evaluation scores will be posted only after the experiments actually run.

## Original challenge

https://community.sundog-education.com/c/monthly-challenges-dive-in/challenge-1-the-codebase-whisperer
