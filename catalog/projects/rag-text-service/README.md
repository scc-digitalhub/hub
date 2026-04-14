# Rag Text Service

This function implements a Retrieval-Augmented Generation (RAG) service that combines document retrieval with large language model inference to provide context-aware text generation. It enables users to query a knowledge base and receive answers grounded in retrieved documents. The service is containerized and runs on Kubernetes, supporting vector similarity search and integration with deployed LLM models.

## Workflow

![RAG Text Service Workflow](https://raw.githubusercontent.com/scc-digitalhub/hub/refs/heads/main/catalog/projects/rag-text-service/workflow.png)

## Features

The `rag-text-service` function includes the following features:

- **Document retrieval**: Semantic search across indexed document collections using vector embeddings
- **LLM integration**: Combines retrieved context with language models for generating contextual responses
- **OpenAI-compatible API**: Provides a REST API endpoint compatible with OpenAI's chat completion format
- **Vector database support**: Efficient storage and retrieval of document embeddings
- **Configurable models**: Deploy various open-source LLMs from Hugging Face Hub
- **Real-time inference**: Stream generated responses based on retrieved context
- **Kubernetes-native**: Containerized deployment with automatic scaling and health monitoring
- **Batch processing**: Handle single and batched query requests efficiently


## Definition

### vllm-text-serve

A VLLM text serving function that deploys and manages large language model inference using the OpenAI-compatible API framework.

**Key specifications:**

- Model: Qwen/Qwen2.5-0.5B-Instruct (from Hugging Face Hub)
- Python version: 3.10
- Purpose: Handles LLM inference requests with streaming support

### embed

A KubeAI text embedding function that generates vector embeddings for documents and queries.

**Key specifications:**

- Model: gte-base (from Hugging Face Hub)
- Engine: VLLM
- Feature: TextEmbedding
- Token limit: The model accepts a maximum input of 512 tokens per request to generate embeddings.

### embedder

This Python batch processing function is responsible for preparing and indexing documents into a vector store database, specifically utilizing PGVectorStore. PGVectorStore is a PostgreSQL extension that enables efficient storage and retrieval of vector embeddings, making it suitable for semantic search and similarity-based queries. The function processes input documents, generates their vector representations (embeddings), and stores them in the PGVectorStore database for subsequent retrieval and analysis.

A Python batch processing function that prepares and indexes documents into the vector store database.

**Key specifications:**

- Python version: 3.10
- Primary dependencies: LangChain, PostgreSQL, OpenAI SDK, BeautifulSoup4
- Purpose: Loads web documents, splits them into chunks, generates embeddings, and stores them in PostgreSQL with pgvector extension

### rag-service

A Python serving function that orchestrates the RAG pipeline, combining document retrieval with LLM-based answer generation.

**Key specifications:**

- Python version: 3.10
- Handler: `src.serve:serve`
- Primary dependencies: LangChain ecosystem, LangGraph, PostgreSQL, OpenAI SDK
- Purpose: Implements the main RAG service with retrieval, prompt engineering, and response generation using an agentic graph workflow

## Usage

For a complete end-to-end example of deploying and using the RAG text service, refer to the usage notebook. The notebook demonstrates:

1. **Project initialization** with digital hub
2. **VLLM service deployment** for LLM inference
3. **Embedding service setup** for semantic search
4. **Text extraction** from PDF documents
5. **Document embedding generation** and vector storage
6. **RAG service deployment** with integrated retrieval and generation
7. **Query execution** against the deployed RAG service

The notebook provides step-by-step instructions and code examples for the complete RAG pipeline workflow.

## Resources

These settings define the resource requests and limits for the runtime.

| Resource | Value | Description |
| -------- | ----- | ----------- |
| **GPU Type** | `V100` or `A100` | GPU accelerator for model inference. |

The `rag-text-service` function requires GPU acceleration to operationalize large language models efficiently. GPU is mandatory for model inference and cannot be replaced by CPU-only computation.
