import logging
from core.vector_store import global_vector_store
from core.prompts import PromptTemplates
from core.llm import LLMEngine
from config.settings import DEFAULT_TOP_K, DEFAULT_TEMPERATURE

logger = logging.getLogger(__name__)

class RAGPipeline:
    @classmethod
    def query(cls, question, mode="Explain", level="Intermediate", top_k=DEFAULT_TOP_K, temperature=DEFAULT_TEMPERATURE, user_id=1, doc_id=None):
        """
        Executes end-to-end RAG pipeline:
        1. Retrieval from VectorStore with user_id and optional doc_id filtering
        2. Grounding check & source citation formatting
        3. Prompt construction with Tutor System Prompt
        4. Generation via LLMEngine
        5. Returns response + citations + transparency info
        """
        # Step 1: Semantic Search Retrieval
        search_results = global_vector_store.search(question, top_k=top_k, user_id=user_id)
        if doc_id:
            search_results = [r for r in search_results if r.get("doc_id") == doc_id]

        # Build context string and source citations
        context_passages = []
        sources = []
        scores = []

        for idx, item in enumerate(search_results):
            context_passages.append(f"[Source {idx+1} | {item['filename']} | Page {item['page_number']}]:\n{item['content']}")
            sources.append({
                "source_id": idx + 1,
                "filename": item["filename"],
                "page_number": item["page_number"],
                "score": item["score"],
                "snippet": item["content"][:150] + "..."
            })
            scores.append(item["score"])

        full_context = "\n\n".join(context_passages) if context_passages else "No relevant study document context found."

        # Grounding & Material check
        has_sufficient_context = len(sources) > 0 and (max(scores) if scores else 0.0) >= 0.25

        # Step 2: System & User Prompt Construction
        system_prompt = PromptTemplates.get_tutor_system_prompt(mode=mode, level=level)
        
        user_prompt = f"""STUDENT QUESTION: {question}

STUDY MATERIAL CONTEXT:
{full_context}

CRITICAL RESPONSE INSTRUCTIONS:
1. Answer ONLY the student's specific question directly, concisely, and accurately based on the study material context.
2. Do NOT dump unrelated sections, subtopics, schemas, or operations from the context unless directly requested by the student's question.
3. Provide a clear, focused explanation proportional to what was asked. Avoid bloated chapter summaries."""

        # Step 3: LLM Generation
        raw_response = LLMEngine.generate(user_prompt, system_prompt=system_prompt, temperature=temperature)

        # If context was lacking, prepend grounding notice if not already present
        if not has_sufficient_context and "couldn't find enough information" not in raw_response.lower():
            final_response = "⚠️ *I couldn't find enough information directly in your uploaded study material for this specific query. Here is a general AI explanation:* \n\n" + raw_response
            grounding_score = 0.35
        else:
            final_response = raw_response
            # Calculate simple grounding confidence score
            avg_score = sum(scores)/len(scores) if scores else 0.0
            grounding_score = round(min(0.98, max(0.40, avg_score + 0.15)), 2)

        # Step 4: Transparency & Explanation Pipeline Info
        transparency_info = {
            "query": question,
            "tutor_mode": mode,
            "level": level,
            "top_k": top_k,
            "retrieved_count": len(search_results),
            "similarity_scores": scores,
            "grounding_confidence": grounding_score,
            "retrieved_chunks": sources,
            "system_prompt_sample": system_prompt[:250] + "...",
            "context_tokens_est": len(full_context.split())
        }

        return {
            "answer": final_response,
            "sources": sources,
            "has_context": has_sufficient_context,
            "grounding_score": grounding_score,
            "transparency": transparency_info
        }
