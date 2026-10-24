import logging
from core.vector_store import global_vector_store
from core.prompts import PromptTemplates
from core.llm import LLMEngine
from database.models import DocumentModel

logger = logging.getLogger(__name__)

class SummaryFeature:
    @classmethod
    def generate_summary(cls, doc_id, depth="Medium"):
        """Generates document summary with Executive Summary, Key Concepts, Formulas, Exam Questions."""
        doc = DocumentModel.get_document_by_id(doc_id)
        if not doc:
            return "Document not found."

        filename = doc["filename"]
        chunks = DocumentModel.get_chunks_for_doc(doc_id)

        if not chunks:
            return "No content found in document to summarize."

        total_chunks = len(chunks)
        
        # Determine maximum target chunks for LLM context based on depth
        if depth == "Short":
            target_count = min(6, total_chunks)
        elif depth == "Detailed":
            target_count = min(35, total_chunks)
        else: # Medium
            target_count = min(15, total_chunks)

        # Sample evenly across the entire document from start to finish
        if total_chunks <= target_count:
            sample_chunks = chunks
        else:
            step = total_chunks / target_count
            sample_indices = [int(i * step) for i in range(target_count)]
            sample_chunks = [chunks[idx] for idx in sample_indices]

        context = "\n\n".join([f"Chunk {c['chunk_index']} (Page {c.get('page_number', 1)}): {c['content']}" for c in sample_chunks])

        prompt = PromptTemplates.get_summary_prompt(context, filename, depth=depth)
        system_prompt = (
            f"You are StudyMind AI Summarization Engine operating at '{depth}' depth level. "
            f"Synthesize comprehensive material covering the ENTIRE document from start to end (Total {total_chunks} chunks)."
        )

        max_tokens = 4096 if depth == "Detailed" else 2048
        summary_md = LLMEngine.generate(prompt, system_prompt=system_prompt, temperature=0.3, max_tokens=max_tokens)
        return summary_md
