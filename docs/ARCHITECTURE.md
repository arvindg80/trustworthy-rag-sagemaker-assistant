# Architecture (incremental)

## Current state — Week 1

~~~mermaid
flowchart TD
    A[AWS SageMaker AI documentation] --> B[PDFs in Unity Catalog Volume]
    B --> C[PyMuPDF page extraction]
    C --> D[Word chunking with overlap]
    D --> E[Delta table with source metadata]
    E --> F[SQL sanity checks]
~~~

## Planned RAG pipeline

~~~mermaid
flowchart LR
    E[Delta chunks] --> V[Embeddings and AI Search]
    Q[User question] --> R[Retriever]
    V --> R
    R --> L[Grounded LLM prompt]
    L --> A[Answer with citations]
    A --> M[MLflow and Ragas evaluation]
~~~

This planned architecture is intentionally not presented as implemented.
