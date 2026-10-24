import streamlit as st
from ui.components import UIComponents

def render_professor_demo_page():
    UIComponents.render_header(
        title="Project Insights & Architecture (Viva Demo)",
        subtitle="Interactive visual breakdown of StudyMind's Generative AI & RAG Pipeline for academic presentation.",
        icon="🧪"
    )

    st.markdown("""
    <div class="sm-card-gradient">
        <h3 style="margin-top: 0; color: #f8fafc;">🎓 Academic Viva & Demonstration Guide</h3>
        <p style="color: #cbd5e1; font-size: 0.98rem; line-height: 1.6;">
            This page explains the internal engineering steps of StudyMind to demonstrate how Generative AI concepts 
            (Document Chunking, Sentence Embeddings, FAISS Vector Search, Prompt Engineering, and RAG Grounding) are implemented end-to-end.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔄 End-to-End RAG Architecture Pipeline")

    # Step Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "1. Document Processing",
        "2. Embedding Generation",
        "3. Vector Store Index",
        "4. Semantic Retrieval",
        "5. Prompt Engineering",
        "6. LLM & Source Citation"
    ])

    with tab1:
        st.markdown("#### Step 1: Document Ingestion & Chunking")
        st.code("""
PDF / DOCX / PPTX / TXT
  ↓ (pypdf / python-docx / python-pptx)
Raw Unstructured Text Extraction
  ↓ (RegEx Cleaning & Whitespace Normalization)
Clean Text Stream
  ↓ (Sliding Window Word Chunking: Chunk Size=600 words, Overlap=100 words)
Structured Chunks with Page Number Metadata
        """, language="text")
        st.info("💡 **Why Chunking?** LLMs have fixed context windows. Chunking splits massive textbooks into targeted passages while preserving surrounding context with overlap.")

    with tab2:
        st.markdown("#### Step 2: Dense Vector Embeddings")
        st.code("""
Text Chunk: "A deadlock is a state where processes are permanently blocked..."
  ↓ (SentenceTransformers model: all-MiniLM-L6-v2)
384-Dimensional Dense Floating-Point Vector:
[ 0.0421, -0.1189, 0.0892, 0.0315, ..., -0.0512 ]
        """, language="text")
        st.info("💡 **Why Embeddings?** Embeddings convert human semantic concepts into mathematical vectors where semantically similar topics are close in vector space.")

    with tab3:
        st.markdown("#### Step 3: FAISS Vector Database Indexing")
        st.code("""
Dense Vectors (N x 384) + Chunk Metadata Dicts
  ↓ (FAISS Inner-Product Index / Cosine Matrix)
Persisted Index Store (data/vectorstore/index_data.pkl)
        """, language="text")
        st.info("💡 **Why Vector DB?** Enables sub-millisecond similarity search across thousands of indexed study pages without querying slow relational databases.")

    with tab4:
        st.markdown("#### Step 4: Semantic Query Retrieval")
        st.code("""
Student Question: "How does deadlock avoidance work?"
  ↓ (SentenceTransformers Query Embedding)
Query Vector (1 x 384)
  ↓ (Cosine Similarity Dot-Product Search against Index Matrix)
Top-K (e.g. K=3) Most Similar Passages Returned with Relevance Scores
        """, language="text")
        st.info("💡 **Why Semantic Search?** Traditional keyword search fails if synonyms are used. Vector search matches meaning regardless of phrasing.")

    with tab5:
        st.markdown("#### Step 5: Structured Prompt Engineering")
        st.code("""
[System Role Prompt]: "You are StudyMind AI Tutor... Tutoring Mode: Exam Mode..."
[Retrieved Context]: "[Source 1 | Operating_Systems.pdf | Page 23]: Deadlock avoidance uses Banker's algorithm..."
[Student Question]: "What is deadlock avoidance?"
  ↓
Constructed Augmented Prompt Sent to LLM
        """, language="text")
        st.info("💡 **Why Role Prompting?** Directs LLM output format (e.g. Socratic mode vs Exam mode vs Simple mode) while constraining knowledge to retrieved context.")

    with tab6:
        st.markdown("#### Step 6: Grounded Generation & Citation Display")
        st.code("""
Augmented Prompt → LLM Engine (Groq Llama-3.3-70B / Smart Local Engine)
  ↓
Synthesized Answer + Source Footnotes + N-gram Grounding Confidence Check
        """, language="text")
        st.success("✅ **Result:** Fully grounded academic response with page-level citations and zero hallucination!")
