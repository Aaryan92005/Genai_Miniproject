# Walkthrough - StudyMind: AI-Powered Personal Learning OS

StudyMind is a functional, startup-grade Generative AI educational platform built using Python, Streamlit, SQLite, Sentence Transformers, FAISS, Plotly, and flexible multi-LLM orchestration.

---

## 🌟 What Was Built

### 1. Core Architecture & Storage
- [config/settings.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/config/settings.py): Central configurations, paths, model choices.
- [database/db.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/database/db.py) & [database/models.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/database/models.py): Persistent SQLite schema for Users, Documents, Chunks, Quiz Attempts, Flashcards, Study Plans, Weak Topics, Badges, and Streaks.

### 2. Core GenAI & RAG Pipeline
- [core/document_processor.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/core/document_processor.py): Text extraction for PDF, DOCX, PPTX, TXT with sliding-window chunking (600 words, 100 word overlap).
- [core/embeddings.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/core/embeddings.py): Dense sentence embedding generation using `all-MiniLM-L6-v2` with TF-IDF fallback vectorizer.
- [core/vector_store.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/core/vector_store.py): Persistent FAISS / Cosine similarity vector index.
- [core/llm.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/core/llm.py): Unified LLM engine supporting Groq API, OpenAI API, HuggingFace, and **Smart Local Fallback Engine** (zero API key dependency).
- [core/prompts.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/core/prompts.py): Role-prompt management for Explain, Teach, Exam, Socratic, Simple modes, Quizzes, Flashcards, Summaries, Study Plans.
- [core/rag.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/core/rag.py): End-to-end RAG orchestrator with grounding confidence scores, citation footnote mapping, and transparency metadata.

### 3. Educational Feature Suite
- [features/chat.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/chat.py): Interactive RAG AI Tutor.
- [features/summaries.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/summaries.py): Executive summaries, key concepts, formulas, exam questions, 1-min revision.
- [features/quiz.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/quiz.py): Dynamic quiz generator & **Adaptive Difficulty Engine** (`████████░░`).
- [features/flashcards.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/flashcards.py): Active recall flip cards & spaced repetition mastery tracking.
- [features/mock_exam.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/mock_exam.py): Timed university exam simulator with performance analysis.
- [features/study_plan.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/study_plan.py): Personalized daily study schedule generator.
- [features/weak_topics.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/weak_topics.py): Weak concept detector & **"Fix My Weakness"** AI revision loop.
- [features/analytics.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/analytics.py): Plotly interactive charts & dynamic AI study insights.
- [features/evaluation.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/features/evaluation.py): BLEU, ROUGE-1, ROUGE-L, Grounding, and Perplexity metrics suite.

### 4. UI/UX Design System & 14 Streamlit Navigation Views
- Custom glassmorphic CSS styling in [ui/styles.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/ui/styles.py).
- Reusable UI component library in [ui/components.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/ui/components.py).
- CS Demo Data Seeder in [utils/seed_demo_data.py](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/utils/seed_demo_data.py).
- 14 complete views: Dashboard, Library, AI Tutor, Semantic Search, Summarize, Quiz Generator, Flashcards, Mock Exam, Study Planner, Analytics, Weak Topics, Responsible AI, How It Works (Viva Demo), Settings.

---

## 🧪 Verification Results

1. **Database & Schema Initialization**: [init_db()](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/database/db.py#15-160) verified successfully creating all 9 tables in [data/studymind.db](file:///c:/Users/91977/Desktop/sem%20VII%20Submissions/Genai/Miniproject/data/studymind.db).
2. **Document Processing & Vector Search**: Tested text extraction, sliding-window chunking, and embedding generation on demo CS files. RAG search successfully retrieved relevant context passages with similarity scores.
3. **Quiz & Flashcard Generation**: Dynamic quiz generation and JSON schema validation tested and verified.
4. **GenAI Evaluation Suite**: Verified calculation of BLEU, ROUGE-1, ROUGE-L, Grounding, and Perplexity metrics.
5. **Smart Local Fallback**: Verified app executes out-of-the-box in fallback mode without crashing when no API key is supplied.

---

## 🚀 How to Run StudyMind

1. Open your terminal in the workspace directory:
   ```bash
   cd "c:\Users\91977\Desktop\sem VII Submissions\Genai\Miniproject"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Open your browser at `http://localhost:8501`.
