import os
import pickle
import logging
import numpy as np
from config.settings import VECTORSTORE_DIR
from core.embeddings import EmbeddingEngine

logger = logging.getLogger(__name__)

INDEX_FILE = VECTORSTORE_DIR / "index_data.pkl"

class VectorStore:
    def __init__(self):
        self.chunks = [] # List of dicts: {'chunk_id', 'doc_id', 'filename', 'page_number', 'content'}
        self.vectors = None # Numpy array (N, dim)
        self.load_index()

    def load_index(self):
        """Loads index metadata and vectors from disk."""
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, "rb") as f:
                    data = pickle.load(f)
                    self.chunks = data.get("chunks", [])
                    self.vectors = data.get("vectors", None)
                logger.info(f"Loaded VectorStore index with {len(self.chunks)} chunks.")
            except Exception as e:
                logger.error(f"Error loading vector index: {e}")
                self.chunks = []
                self.vectors = None

    def save_index(self):
        """Saves vectors and chunk metadata to disk."""
        try:
            with open(INDEX_FILE, "wb") as f:
                pickle.dump({
                    "chunks": self.chunks,
                    "vectors": self.vectors
                }, f)
            logger.info(f"Saved VectorStore index with {len(self.chunks)} chunks.")
        except Exception as e:
            logger.error(f"Error saving vector index: {e}")

    def add_chunks(self, doc_id, filename, chunks_list, user_id=1):
        """
        Adds chunk dicts [{'chunk_index': int, 'page_number': int, 'content': str}]
        """
        if not chunks_list:
            return

        # Deduplicate: Remove existing chunks for this doc_id if re-indexed
        keep_indices = []
        for i, c in enumerate(self.chunks):
            if not (c.get("doc_id") == doc_id and c.get("user_id") == user_id):
                keep_indices.append(i)

        if len(keep_indices) < len(self.chunks):
            self.chunks = [self.chunks[i] for i in keep_indices]
            if self.vectors is not None and self.vectors.shape[0] > 0:
                self.vectors = self.vectors[keep_indices]

        texts = [c['content'] for c in chunks_list]
        new_vecs = EmbeddingEngine.embed_texts(texts)

        for c in chunks_list:
            self.chunks.append({
                "doc_id": doc_id,
                "user_id": user_id,
                "filename": filename,
                "chunk_index": c["chunk_index"],
                "page_number": c.get("page_number", 1),
                "content": c["content"]
            })

        if self.vectors is None or self.vectors.shape[0] == 0:
            self.vectors = new_vecs
        else:
            self.vectors = np.vstack([self.vectors, new_vecs])

        self.save_index()

    def search(self, query, top_k=5, user_id=None, min_threshold=0.25):
        """
        Performs hybrid vector similarity + keyword search filtering by user_id.
        Deduplicates identical chunks and enforces a minimum relevance threshold.
        """
        if not self.chunks or self.vectors is None or self.vectors.shape[0] == 0:
            return []

        # Filter candidate indices by user_id if requested
        valid_indices = []
        for i, chunk in enumerate(self.chunks):
            chunk_u_id = chunk.get("user_id", 1)
            if user_id is None or chunk_u_id == user_id:
                valid_indices.append(i)

        if not valid_indices:
            return []

        query_vec = EmbeddingEngine.embed_query(query)
        sub_vectors = self.vectors[valid_indices]
        raw_scores = np.dot(sub_vectors, query_vec)

        query_terms = [t.lower().strip() for t in query.split() if len(t.strip()) > 1]

        scored_results = []
        seen_contents = set()

        for sub_idx, orig_idx in enumerate(valid_indices):
            chunk = self.chunks[orig_idx]
            content_str = chunk["content"].strip()
            content_lower = content_str.lower()

            # Deduplication check
            if content_str in seen_contents:
                continue

            raw_sc = float(raw_scores[sub_idx])
            # Normalize cosine similarity to [0, 1]
            norm_score = max(0.0, min(1.0, (raw_sc + 1.0) / 2.0 if raw_sc < 0 else raw_sc))

            # Hybrid Keyword Match Boost
            keyword_matches = sum(1 for term in query_terms if term in content_lower)
            if keyword_matches > 0:
                keyword_boost = 0.25 * (keyword_matches / len(query_terms))
                final_score = min(1.0, norm_score + keyword_boost)
            else:
                final_score = norm_score

            # Enforce Minimum Threshold unless exact keyword was found
            if final_score >= min_threshold or (keyword_matches > 0 and final_score >= 0.20):
                seen_contents.add(content_str)
                scored_results.append({
                    "doc_id": chunk["doc_id"],
                    "filename": chunk["filename"],
                    "page_number": chunk["page_number"],
                    "content": chunk["content"],
                    "score": round(final_score, 3)
                })

        # Sort by final relevance score descending
        scored_results.sort(key=lambda x: x["score"], reverse=True)

        return scored_results[:top_k]

    def delete_document(self, doc_id):
        """Removes all chunks and vectors belonging to a specific doc_id."""
        if not self.chunks:
            return

        keep_indices = [i for i, c in enumerate(self.chunks) if c.get("doc_id") != doc_id]
        if len(keep_indices) < len(self.chunks):
            self.chunks = [self.chunks[i] for i in keep_indices]
            if self.vectors is not None and self.vectors.shape[0] > 0:
                self.vectors = self.vectors[keep_indices]
            self.save_index()

    def clear(self):
        """Clears vector index."""
        self.chunks = []
        self.vectors = None
        if INDEX_FILE.exists():
            os.remove(INDEX_FILE)

    def get_chunk_count(self):
        return len(self.chunks)

# Singleton global instance
global_vector_store = VectorStore()
