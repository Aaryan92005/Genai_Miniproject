# StudyMind – AI-Powered Personal Learning OS 🧠

> **"Your AI-powered personal learning companion"**  
> *A Production-Grade Generative AI Educational Platform built for College Mini-Projects & Academic Excellence.*

---

## 📌 1. Project Overview

**StudyMind** is an end-to-end Generative AI educational operating system designed to turn student study materials—lecture notes, PDFs, textbooks, PPT/PPTX slides, and syllabi—into a dynamic personal AI tutor and learning environment.

Unlike static UI prototypes or hardcoded chatbots, **StudyMind is fully functional**, incorporating:
- **Document Chunking & Ingestion Engine** (PDF, DOCX, PPTX, TXT)
- **Dense Vector Search** using sentence embeddings and FAISS / Cosine similarity indexing
- **Retrieval-Augmented Generation (RAG)** with strict source citations and page numbers
- **AI Tutor Modes**: Explain, Teach, Exam, Socratic (guiding questions), and Simple modes
- **Explanation Levels**: Beginner, Intermediate, and Advanced
- **Dynamic & Adaptive AI Quizzes**: Auto-generates MCQs, True-False, and Short Answer questions with difficulty scaling based on live accuracy
- **Smart Flashcards**: Active recall deck with flip cards, I Know / Review Again tracking, and spaced repetition mastery scores
- **Timed Mock Examination Mode**: Distraction-free exam simulator with score breakdown, strong/weak topic analysis, and AI feedback
- **Personalized AI Study Planner**: Dynamic daily schedule adapted to exam target dates and student weak areas
- **Weak Topic Detection & "Fix My Weakness"**: Auto-identifies error-prone concepts and generates remedial learning packages
- **Plotly Analytics Dashboard**: Visual tracking of quiz accuracy trends, study hours, topic mastery, and dynamic AI insights
- **Responsible AI Transparency**: Grounding confidence scores, source citations, and local data erasure controls
- **GenAI Evaluation Suite**: Computes BLEU, ROUGE-1, ROUGE-L, Grounding, and Perplexity metrics for academic evaluation
- **Professor Demonstration Mode ("How It Works")**: Interactive visual breakdown of the GenAI pipeline for viva presentation

---

## 🏗️ 2. System Architecture

```
                                  [ User Study Material ]
                            (PDF / DOCX / PPTX / Textbooks / Notes)
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │ Document Processor  │
                                  │  - Text Extraction  │
                                  │  - Cleaning         │
                                  │  - Chunking (600w)  │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │  Embedding Engine   │
                                  │ (all-MiniLM-L6-v2)  │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │   Vector Database   │
                                  │ (FAISS Index / PKL) │
                                  └──────────┬──────────┘
                                             │
                                             ▼
┌──────────────────┐               ┌─────────────────────┐
│  Student Query   ├──────────────►│ Semantic Retrieval  │
└──────────────────┘               │ (Top-K Similarity)  │
                                   └──────────┬──────────┘
                                              │ (Retrieved Chunks + Scores)
                                              ▼
                                   ┌─────────────────────┐
                                   │ Prompt Engineering  │
                                   │ (Role & System Context)
                                   └──────────┬──────────┘
                                              │
                                              ▼
                                   ┌─────────────────────┐               ┌───────────────────────┐
                                   │     LLM Engine      ├──────────────►│ Grounding Check &     │
                                   │ (Groq/OpenAI/Local) │               │ Source Citations      │
                                   └─────────────────────┘               └──────────┬────────────┘
                                                                                    │
                                                                                    ▼
                                                                         [ AI Tutor Answer +      ]
                                                                         [ Page Footnotes +       ]
                                                                         [ Transparency Metadata  ]
```

---

## 🛠️ 3. Technology Stack

- **Frontend & UI**: Streamlit with Custom Modern Glassmorphic CSS Design System
- **Backend Logic**: Python 3.9+
- **Document Processing**: `pypdf`, `python-docx`, `python-pptx`
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`) with TF-IDF fallback vectorizer
- **Vector Database**: FAISS / Cosine Matrix vector store
- **LLM Integrations**: Groq API (`llama-3.3-70b`), OpenAI API (`gpt-3.5-turbo`), and **Smart Local Fallback LLM** (zero external key dependency)
- **Database & Persistence**: SQLite 3 (`data/studymind.db`)
- **Data Visualization**: Plotly Express & Plotly Graph Objects
- **GenAI Evaluation**: BLEU (NLTK), ROUGE (`rouge-score`), Grounding Score & Perplexity Entropy estimation

---

## 📂 4. Project Folder Structure

```
studymind/
├── app.py                      # Main Streamlit application entry point & router
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── README.md                   # Complete documentation & viva guide
│
├── config/
│   └── settings.py             # System paths, model parameters, API configs
│
├── core/
│   ├── document_processor.py   # PDF/DOCX/PPTX parsing & sliding-window chunking
│   ├── embeddings.py           # SentenceTransformers embedding engine
│   ├── vector_store.py         # FAISS vector store & similarity search
│   ├── llm.py                  # Multi-LLM caller + Smart Local Fallback mode
│   ├── prompts.py              # Structured prompt templates for all modes
│   └── rag.py                  # End-to-end RAG pipeline & transparency logger
│
├── database/
│   ├── db.py                   # SQLite connection engine & table migrations
│   └── models.py               # ORM domain models (Users, Docs, Quizzes, Cards, Plans)
│
├── features/
│   ├── chat.py                 # RAG AI Tutor chat handler
│   ├── summaries.py            # Executive summaries, formulas & exam questions
│   ├── quiz.py                 # Quiz generator & Adaptive Difficulty engine
│   ├── flashcards.py           # Smart flashcards & spaced repetition mastery
│   ├── mock_exam.py            # Timed mock exam evaluator & performance report
│   ├── study_plan.py           # AI Study Planner & task schedule manager
│   ├── weak_topics.py          # Weak area detector & "Fix My Weakness" revision
│   ├── analytics.py            # Plotly charts & dynamic AI insights
│   └── evaluation.py           # BLEU, ROUGE, Grounding & Perplexity evaluation
│
├── ui/
│   ├── styles.py               # Custom dark/glassmorphic CSS theme
│   ├── components.py           # Metric cards, chips, transparency accordions
│   └── pages/                  # Streamlit view modules for all 14 menu screens
│       ├── dashboard_view.py
│       ├── library_view.py
│       ├── tutor_view.py
│       ├── search_view.py
│       ├── summarize_view.py
│       ├── quiz_view.py
│       ├── flashcards_view.py
│       ├── mock_exam_view.py
│       ├── study_planner_view.py
│       ├── analytics_view.py
│       ├── weak_topics_view.py
│       ├── responsible_ai_view.py
│       ├── settings_view.py
│       └── professor_demo_view.py
│
├── data/                       # Persistent local storage (Git ignored)
│   ├── uploads/
│   ├── vectorstore/
│   ├── demo_files/
│   └── studymind.db
│
└── utils/
    └── seed_demo_data.py       # CS study materials auto-seeder
```

---

## ⚡ 5. Setup & Local Execution Guide

### Step 1: Navigate to Workspace
```bash
cd "c:\Users\91977\Desktop\sem VII Submissions\Genai\Miniproject"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional: Add your `GROQ_API_KEY` or `OPENAI_API_KEY`. If left empty, StudyMind operates in **Smart Local Fallback Mode** automatically with zero crashes!)*

### Step 4: Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎓 6. Academic Alignment & GenAI Concepts Demonstrated

1. **Document Processing**: Text extraction, regex normalization, sliding-window chunking with overlap.
2. **Transformers & Embeddings**: Dense vector spaces (`all-MiniLM-L6-v2`), vector normalization, cosine distance scoring.
3. **Vector Database**: High-performance indexed vector storage using FAISS and pickle persistence.
4. **Retrieval-Augmented Generation (RAG)**: Eliminates hallucinations by retrieving grounded document context before prompt construction.
5. **Prompt Engineering**: Socratic tutoring, role-based prompting, structured JSON schema generation.
6. **Adaptive Learning**: Dynamic quiz difficulty adjustment based on student performance history.
7. **Responsible AI**: Grounding confidence indices, source citations (filename + page numbers), data privacy, and local data deletion.
8. **GenAI Evaluation**: BLEU, ROUGE-1, ROUGE-L, Grounding Score, and Perplexity entropy estimation.

---

## 🏆 7. Professor Viva Demonstration Checklist

During your project demonstration / viva examination, show these key workflows:
1. **Dashboard**: Show streak, study hours, quiz accuracy, level badge, and AI insight card.
2. **Document Library**: Upload a new PDF/DOCX or demonstrate pre-seeded CS study files.
3. **AI Tutor**: Ask *"What is deadlock prevention?"* and test **Socratic Mode** and **Exam Mode**. Show source citations and expand **"🔍 How StudyMind Answered"** transparency accordion.
4. **Quiz Generator**: Generate a 5-question quiz, enable **Adaptive Difficulty**, answer questions, and view instant feedback with explanations and source citations.
5. **Smart Flashcards**: Flip cards, mark *"I Know This"*, and show mastery score updates.
6. **Weak Topic Detection**: Click **"Fix My Weakness"** to show targeted AI remedial breakdown.
7. **Analytics**: Show interactive Plotly accuracy trend line chart and study hours distribution.
8. **Project Insights (Viva Page)**: Open the **"🧪 How It Works"** page to explain the 6-stage GenAI pipeline to your professor!
