import logging
import numpy as np
from config.settings import EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)

_transformer_model = None
_tfidf_vectorizer = None

class EmbeddingEngine:
    @classmethod
    def get_model(cls):
        global _transformer_model
        if _transformer_model is None:
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
                logger.info(f"Loading SentenceTransformer model: {EMBEDDING_MODEL_NAME}")
                _transformer_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer ({e}). Using TF-IDF Fallback Vectorizer.")
                _transformer_model = "TFIDF_FALLBACK"
        return _transformer_model

    @classmethod
    def embed_texts(cls, texts):
        """
        Computes normalized embedding vectors for a list of string texts.
        Returns numpy array of shape (N, dim).
        """
        if not texts:
            return np.zeros((0, 384), dtype=np.float32)

        model = cls.get_model()

        if model != "TFIDF_FALLBACK" and hasattr(model, "encode"):
            try:
                embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
                return embeddings.astype(np.float32)
            except Exception as e:
                logger.warning(f"Error encoding with SentenceTransformer: {e}. Falling back to TF-IDF.")

        # TF-IDF Fallback
        from sklearn.feature_extraction.text import TfidfVectorizer
        global _tfidf_vectorizer
        if _tfidf_vectorizer is None or len(texts) > 1:
            _tfidf_vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
            matrix = _tfidf_vectorizer.fit_transform(texts).toarray()
        else:
            try:
                matrix = _tfidf_vectorizer.transform(texts).toarray()
            except Exception:
                _tfidf_vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
                matrix = _tfidf_vectorizer.fit_transform(texts).toarray()

        # Normalize rows
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        normalized = (matrix / norms).astype(np.float32)
        
        # Pad to 384 dimensions if fewer features extracted
        if normalized.shape[1] < 384:
            padding = np.zeros((normalized.shape[0], 384 - normalized.shape[1]), dtype=np.float32)
            normalized = np.hstack([normalized, padding])
            
        return normalized

    @classmethod
    def embed_query(cls, query):
        """Embeds a single text query."""
        vecs = cls.embed_texts([query])
        return vecs[0] if len(vecs) > 0 else np.zeros((384,), dtype=np.float32)
