import json
import logging
import re
from core.vector_store import global_vector_store
from core.prompts import PromptTemplates
from core.llm import LLMEngine
from database.models import FlashcardModel, DocumentModel

logger = logging.getLogger(__name__)

class FlashcardFeature:
    @classmethod
    def generate_cards(cls, topic, doc_id=None, num_cards=5, user_id=1):
        """Generates AI flashcards from vector store context and saves to database."""
        if doc_id:
            chunks = DocumentModel.get_chunks_for_doc(doc_id)
            context = "\n\n".join([c["content"] for c in chunks[:12]]) if chunks else f"Study material for {topic}."
        else:
            search_results = global_vector_store.search(topic, top_k=6, user_id=user_id)
            if not search_results:
                search_results = global_vector_store.search("core concepts summary", top_k=6, user_id=user_id)
            context = "\n\n".join([s["content"] for s in search_results]) if search_results else f"Study material for {topic}."

        prompt = PromptTemplates.get_flashcard_prompt(context, topic, num_cards=num_cards)
        system_prompt = "You are StudyMind AI Flashcard Engine. Output strictly valid JSON arrays of high-yield study flashcards."

        raw = LLMEngine.generate(prompt, system_prompt=system_prompt, json_mode=True, max_tokens=2048)

        try:
            clean_raw = re.sub(r'^```json\s*', '', raw, flags=re.MULTILINE)
            clean_raw = re.sub(r'^```\s*', '', clean_raw, flags=re.MULTILINE).strip()
            cards_data = json.loads(clean_raw)
            if not isinstance(cards_data, list):
                cards_data = [cards_data]
        except Exception:
            cards_data = json.loads(LLMEngine._generate_fallback_json(f"flashcard topic {topic}"))

        # Save to DB for this specific user
        formatted_cards = []
        for c in cards_data:
            formatted_cards.append({
                "doc_id": doc_id,
                "topic": topic,
                "question": c.get("question", f"What is key concept in {topic}?"),
                "answer": c.get("answer", f"Core principle of {topic}."),
                "difficulty": c.get("difficulty", "Medium")
            })

        FlashcardModel.add_flashcards(formatted_cards, user_id=user_id)
        return FlashcardModel.get_cards(topic=topic, user_id=user_id)

    @classmethod
    def get_cards_for_topic(cls, topic="All Topics", user_id=1):
        """Returns existing cards from DB or generates a new deck if empty."""
        cards = FlashcardModel.get_cards(topic=topic, user_id=user_id)
        return cards

    @classmethod
    def record_review(cls, card_id, knew_it=True, user_id=1):
        """Updates flashcard mastery score in DB."""
        FlashcardModel.update_mastery(card_id, knew_it, user_id=user_id)
