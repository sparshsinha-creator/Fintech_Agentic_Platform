# RAG_DESIGN.md

# MyFinance - Retrieval-Augmented Generation (RAG) Design

## Purpose

This document defines the Retrieval-Augmented Generation (RAG) architecture for the MyFinance platform.

The RAG system enables the AI to answer financial questions using reliable knowledge sources rather than relying solely on the language model.

The design focuses on accuracy, explainability, scalability, and maintainability.

---

# Objectives

The RAG system should:

- Retrieve relevant financial information.
- Ground AI responses in trusted documents.
- Reduce hallucinations.
- Support semantic search.
- Scale to large document collections.
- Support future document sources.

---

# High-Level Architecture

```text
                Financial Documents
                         │
                         ▼
              Document Ingestion Pipeline
                         │
                         ▼
                 Text Extraction Layer
                         │
                         ▼
                 Text Preprocessing
                         │
                         ▼
                  Chunk Generation
                         │
                         ▼
                 Embedding Generation
                         │
                         ▼
                     FAISS Index
                         │
                         ▼
                  Semantic Retriever
                         │
                         ▼
                 Context Construction
                         │
                         ▼
                    Gemini LLM
                         │
                         ▼
                  Final AI Response
```

---

# Knowledge Sources

Initial sources include:

- RBI Annual Reports
- Monetary Policy Reports
- Financial Stability Reports
- Government Tax Guidelines
- Investment Guides
- Personal Finance Books
- User Uploaded Documents

Future sources:

- SEBI Circulars
- Mutual Fund Documents
- Stock Market Reports
- Insurance Policies
- Bank Statements

---

# Document Pipeline

Every document passes through:

1. Upload
2. Validation
3. Text Extraction
4. Cleaning
5. Chunking
6. Embedding
7. Vector Storage
8. Metadata Storage

---

# Supported Document Types

- PDF
- TXT
- DOCX
- CSV
- XLSX
- Markdown

Future support:

- Images (OCR)
- HTML
- Web Pages

---

# Text Extraction

Responsibilities

- Read document
- Preserve headings
- Preserve tables where possible
- Remove unnecessary whitespace
- Remove unsupported formatting

---

# Text Preprocessing

Tasks

- Normalize whitespace
- Remove duplicate content
- Preserve important formatting
- Keep section titles
- Preserve page references when available

---

# Chunking Strategy

Primary Strategy

Recursive Character Text Splitting

Recommended Defaults

```text
Chunk Size: 1000 characters

Chunk Overlap: 200 characters
```

Alternative strategies may include:

- Sentence-based chunking
- Semantic chunking
- Section-aware chunking

---

# Embedding Generation

Purpose

Convert text chunks into vector embeddings.

Requirements

- Deterministic embeddings
- High semantic quality
- Configurable embedding model

Embedding model should be configurable through environment variables.

---

# Vector Database

Technology

FAISS

Responsibilities

- Store embeddings
- Perform similarity search
- Return Top-K results

Future support:

- ChromaDB
- Pinecone
- Weaviate
- Milvus

---

# Metadata

Every indexed chunk should include:

- Document ID
- Document Name
- Source
- Page Number
- Section Title
- Chunk ID
- Timestamp

Example

```json
{
  "document": "RBI Annual Report 2025",
  "page": 42,
  "section": "Inflation",
  "chunk_id": 105
}
```

---

# Retrieval Process

User Query

↓

Embedding Generation

↓

Similarity Search

↓

Top-K Results

↓

Context Builder

↓

Gemini

↓

Final Response

---

# Context Builder

Responsibilities

- Merge retrieved chunks
- Remove duplicates
- Respect context window
- Preserve source information

The context should be concise, relevant, and ordered by similarity.

---

# Retrieval Parameters

Default values:

```text
Top K Results = 5

Similarity Metric = Cosine Similarity

Minimum Similarity Threshold = Configurable
```

These values should be configurable.

---

# Prompt Construction

Prompt should contain:

- User question
- Retrieved context
- System instructions
- Response format requirements

The model should answer using the provided context whenever possible.

---

# Source Attribution

Whenever practical, responses should include references such as:

- Document Name
- Page Number
- Section Title

This improves explainability and user trust.

---

# Error Handling

If no relevant context is found:

- Notify the user.
- Avoid fabricating information.
- Optionally answer using general model knowledge while indicating that no supporting documents were found.

---

# Performance Guidelines

- Cache frequent queries.
- Reuse embeddings when possible.
- Batch embedding operations.
- Index documents asynchronously.
- Avoid duplicate indexing.

---

# Security

Never expose:

- Internal document paths
- Sensitive metadata
- User-uploaded confidential files

Restrict document access based on user permissions.

---

# Future Enhancements

- Hybrid Search (Keyword + Semantic)
- Query Rewriting
- Reranking Models
- Multi-Vector Retrieval
- Graph RAG
- Knowledge Graph Integration
- Incremental Index Updates
- Multi-language Retrieval

---

# Current Status

Current Phase

Architecture Planning

Implementation will begin after:

- FastAPI Foundation
- Database Layer
- LangGraph Integration

This document serves as the official design specification for the RAG subsystem.