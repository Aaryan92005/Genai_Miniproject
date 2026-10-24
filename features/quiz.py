import json
import logging
import re
from core.vector_store import global_vector_store
from core.prompts import PromptTemplates
from core.llm import LLMEngine
from database.models import QuizModel, DocumentModel

logger = logging.getLogger(__name__)

class QuizFeature:
    @classmethod
    def generate_quiz(cls, topic, doc_id=None, num_questions=5, difficulty="Medium", question_type="MCQ", user_id=1):
        """Generates dynamic quiz questions with strict document grounding and accuracy validation."""
        if doc_id:
            chunks = DocumentModel.get_chunks_for_doc(doc_id)
            total = len(chunks)
            if total > 0:
                # Sample evenly across document chunks
                target_count = min(15, total)
                step = total / target_count
                indices = [int(i * step) for i in range(target_count)]
                context = "\n\n".join([f"Passage {c['chunk_index']} (Page {c.get('page_number', 1)}): {c['content']}" for c in [chunks[i] for i in indices]])
            else:
                context = f"Study material for {topic}."
        else:
            search_results = global_vector_store.search(topic, top_k=6, user_id=user_id)
            context = "\n\n".join([f"Passage: {s['content']}" for s in search_results]) if search_results else f"Topic material for {topic}."

        prompt = PromptTemplates.get_quiz_generation_prompt(
            context=context,
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty,
            question_type=question_type
        )
        system_prompt = "You are StudyMind AI Quiz Generator. Output strictly valid JSON arrays of accurate quiz questions."

        raw = LLMEngine.generate(prompt, system_prompt=system_prompt, json_mode=True, max_tokens=3000)

        try:
            clean_raw = re.sub(r'^```json\s*', '', raw, flags=re.MULTILINE)
            clean_raw = re.sub(r'^```\s*', '', clean_raw, flags=re.MULTILINE).strip()
            
            questions = json.loads(clean_raw)
            if not isinstance(questions, list):
                questions = [questions]
        except Exception as e:
            logger.warning(f"Error parsing quiz JSON ({e}). Utilizing fallback quiz structure.")
            questions = json.loads(LLMEngine._generate_fallback_json(f"quiz topic {topic}"))

        # Post-validation to guarantee option string accuracy
        for q in questions:
            opts = q.get("options", [])
            corr = q.get("correct_answer", "")
            if opts and corr not in opts:
                # Find closest option match if text varies slightly
                match = next((o for o in opts if corr.lower() in o.lower() or o.lower() in corr.lower()), opts[0])
                q["correct_answer"] = match

        return questions

    @classmethod
    def calculate_adaptive_difficulty(cls, current_difficulty, is_correct, consecutive_correct=0, consecutive_wrong=0):
        """
        Adaptive difficulty adjustment rule engine.
        Increases difficulty when correct, decreases or recommends concept revision when incorrect.
        """
        levels = ["Easy", "Medium", "Hard"]
        current_idx = levels.index(current_difficulty) if current_difficulty in levels else 1

        if is_correct:
            consecutive_correct += 1
            consecutive_wrong = 0
            if consecutive_correct >= 2 and current_idx < 2:
                current_idx += 1
                consecutive_correct = 0
        else:
            consecutive_wrong += 1
            consecutive_correct = 0
            if consecutive_wrong >= 1 and current_idx > 0:
                current_idx -= 1

        new_diff = levels[current_idx]
        diff_bar = {
            "Easy": "███░░░░░░░ 30%",
            "Medium": "██████░░░░ 60%",
            "Hard": "█████████░ 90%"
        }.get(new_diff, "██████░░░░ 60%")

        return new_diff, diff_bar, consecutive_correct, consecutive_wrong

    @classmethod
    def save_quiz_results(cls, topic, difficulty, question_type, score, max_score, time_taken_sec, details, user_id=1):
        """Saves completed quiz results to SQLite DB for user."""
        return QuizModel.save_quiz_attempt(
            user_id=user_id,
            topic=topic,
            difficulty=difficulty,
            question_type=question_type,
            score=score,
            max_score=max_score,
            time_taken_sec=time_taken_sec,
            details=details
        )
