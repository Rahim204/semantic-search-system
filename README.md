# AI-Powered Semantic Search System

## Overview

The AI-Powered Semantic Search System is a Python-based application designed to retrieve relevant information from large documents based on the **meaning and context of a user's query**, rather than relying solely on exact keyword matching.

Traditional search techniques such as TF-IDF primarily depend on word overlap, which can make it difficult to retrieve relevant information when a query uses different terminology from the source document. This project addresses that limitation using semantic embeddings and vector similarity.

The system uses the `all-MiniLM-L6-v2` Sentence Transformer model to convert document passages and user queries into 384-dimensional numerical vectors. It then applies cosine similarity to identify and rank the passages most closely related to the user's query.

To process large documents efficiently, the application divides extracted text into smaller, overlapping chunks. It retrieves the top three most similar chunks and calculates their average similarity score to estimate the document's relevance to the requested topic.

## Key Features

- **Semantic Search:** Retrieves relevant passages based on contextual meaning rather than exact keyword matches.
- **Document Chunking:** Divides large documents into smaller, overlapping text sections.
- **Text Embeddings:** Uses Sentence Transformers to represent text as numerical vectors.
- **Cosine Similarity:** Measures similarity between the user's query and document passages.
- **Top-3 Score Aggregation:** Averages the three highest similarity scores to provide a relevance indicator.
- **Document Relevance Assessment:** Uses similarity scores and the application's scoring rules to estimate how relevant a document is to a search topic.

## Technologies Used

- Python
- Sentence Transformers
- `all-MiniLM-L6-v2`
- NumPy
- TF-IDF for traditional keyword-search comparison
- Cosine Similarity

## How It Works

1. **Document Ingestion:** Extracts text from the source document.
2. **Chunking:** Divides the extracted text into smaller, overlapping sections.
3. **Embedding Generation:** Converts each text chunk into a 384-dimensional vector.
4. **Query Processing:** Converts the user's search query into a vector using the same embedding model.
5. **Similarity Calculation:** Compares the query vector with document vectors using cosine similarity.
6. **Ranking and Aggregation:** Ranks the retrieved passages and calculates the average of the top three similarity scores.
7. **Relevance Assessment:** Produces relevant search results and a document relevance indicator based on the implemented scoring logic.

## Applications

- Searching technical books and networking documentation.
- Retrieving relevant information from educational materials.
- Searching research papers and technical reports.
- Building intelligent document retrieval and question-answering systems.
- Serving as a retrieval component for Retrieval-Augmented Generation (RAG) applications.

## Future Enhancements

- Integrate a large language model to generate answers grounded in retrieved passages.
- Add a vector database for scalable document storage and retrieval.
- Support multiple document formats and document collections.
- Display source page numbers and relevant text excerpts.
- Improve relevance assessment using evaluation datasets and calibrated scoring thresholds.
- Develop a web interface for document uploads and interactive searches.

## Conclusion

This project demonstrates how semantic embeddings and vector similarity can improve information retrieval from large documents. By combining document chunking, Sentence Transformers, cosine similarity, and relevance scoring, the system provides a foundation for intelligent search applications and future RAG-based solutions.
