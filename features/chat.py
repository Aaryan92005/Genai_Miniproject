import logging
from core.rag import RAGPipeline

logger = logging.getLogger(__name__)

class ChatFeature:
    @staticmethod
    def process_user_query(question, mode="Explain", level="Intermediate", top_k=3, temperature=0.2, user_id=1, doc_id=None):
        """Processes a chat question through the RAG pipeline with user_id and doc_id filtering."""
        if not question or not question.strip():
            return None

        result = RAGPipeline.query(
            question=question.strip(),
            mode=mode,
            level=level,
            top_k=top_k,
            temperature=temperature,
            user_id=user_id,
            doc_id=doc_id
        )
        return result
