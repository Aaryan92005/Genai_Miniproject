import streamlit as st
from ui.components import UIComponents
from database.db import get_connection

def render_responsible_ai_page():
    UIComponents.render_header(
        title="Responsible AI & Grounding Transparency",
        subtitle="Ethical AI principles, hallucination mitigation, source citation policies, and data privacy controls.",
        icon="⚖️"
    )

    st.markdown("""
    <div class="sm-card-gradient">
        <h3 style="margin-top: 0; color: #f8fafc;">🛡️ Responsible AI Core Directives</h3>
        <p style="color: #cbd5e1; font-size: 0.98rem; line-height: 1.6;">
            StudyMind is architected around <b>Strict RAG Grounding</b> to prevent academic hallucination.
            Every generated explanation prioritizes uploaded course material over pre-trained model biases.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📄 1. Source Citation Integrity
        * **Verifiable Footnotes**: Answers display exact source document filenames and page numbers.
        * **Snippet Verification**: Students can view the raw retrieved passage alongside generated explanations.
        * **No Pretense Policy**: If context is missing, StudyMind explicitly states: *"I couldn't find enough information in your uploaded study material."*
        """)

        st.markdown("""
        ### 🧠 2. Hallucination Awareness
        * **Grounding Score Index**: Each answer evaluates n-gram overlap between retrieved context and output.
        * **Low-Confidence Warnings**: Outputs with confidence scores < 40% are flagged with warning badges.
        """)

    with col2:
        st.markdown("""
        ### 🔒 3. Data Privacy & Local Control
        * **Zero Remote Storage**: Your study notes, PDFs, vector indexes, and database logs remain stored 100% locally on your computer.
        * **No Telemetry**: No user text or uploaded files are sent to third parties for model training.
        * **Data Erasure**: You maintain complete control to purge your data instantly at any time.
        """)

        st.markdown("""
        ### ⚠️ Academic Advisory Notice
        > **Academic Disclaimer:** AI-generated explanations and quizzes are supplementary learning tools. Always verify critical definitions, formulas, and academic claims with your university course materials.
        """)

    st.markdown("---")
    st.markdown("### 🗑️ Data Privacy & Erasure Controls")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔴 Clear All Indexed Documents", key="btn_clear_docs"):
            conn = get_connection()
            conn.execute("DELETE FROM documents")
            conn.execute("DELETE FROM document_chunks")
            conn.commit()
            conn.close()
            st.success("All indexed documents cleared from local database.")

    with col_btn2:
        if st.button("🔴 Reset Learning History & Quizzes", key="btn_clear_history"):
            conn = get_connection()
            conn.execute("DELETE FROM quiz_attempts")
            conn.execute("DELETE FROM flashcards")
            conn.execute("DELETE FROM weak_topics")
            conn.commit()
            conn.close()
            st.success("Learning performance history reset successfully.")
