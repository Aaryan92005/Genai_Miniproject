import streamlit as st
from pathlib import Path
from ui.components import UIComponents
from config.settings import UPLOADS_DIR
from core.document_processor import DocumentProcessor
from core.vector_store import global_vector_store
from database.models import DocumentModel

def render_library_page():
    UIComponents.render_header(
        title="My Document Library",
        subtitle="Upload and manage lecture notes, textbooks, PDFs, and syllabus materials.",
        icon="📚"
    )

    user = st.session_state.get("authenticated_user", {})
    user_id = user.get("id", 1)

    # File Upload Section
    st.markdown("### 📤 Upload Study Material")
    uploaded_file = st.file_uploader(
        "Select PDF, DOCX, PPTX, or TXT file to index into StudyMind",
        type=["pdf", "docx", "pptx", "txt"],
        help="Files are processed, chunked, embedded, and stored locally in your vector database."
    )

    if uploaded_file is not None:
        if st.button("🚀 Process & Index Document", key="btn_process_upload"):
            with st.spinner("Reading document, extracting text, generating embeddings & vector indexing..."):
                save_path = UPLOADS_DIR / uploaded_file.name
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                try:
                    processed = DocumentProcessor.process_and_chunk(save_path)
                    ext = save_path.suffix.replace(".", "").lower()

                    doc_id = DocumentModel.add_document(
                        filename=uploaded_file.name,
                        file_type=ext,
                        file_size=uploaded_file.size,
                        page_count=processed["page_count"],
                        chunk_count=len(processed["chunks"]),
                        topics=["Uploaded Document"],
                        summary={"Executive Summary": f"Document indexed with {len(processed['chunks'])} chunks."},
                        user_id=user_id
                    )

                    global_vector_store.add_chunks(doc_id, uploaded_file.name, processed["chunks"], user_id=user_id)
                    DocumentModel.add_chunks(doc_id, processed["chunks"], user_id=user_id)

                    st.success(f"Successfully processed `{uploaded_file.name}` into {len(processed['chunks'])} vector chunks!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing document: {e}")

    st.markdown("---")

    # Document Cards List
    st.markdown("### 📄 Indexed Study Documents")
    docs = DocumentModel.get_all_documents(user_id=user_id)

    if not docs:
        st.info("No study materials uploaded yet. Upload a document or check out our pre-indexed demo files!")
        return

    for doc in docs:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**📄 {doc['filename']}**")
                st.caption(f"Type: `{doc['file_type'].upper()}` | Pages: {doc['page_count']} | Chunks: {doc['chunk_count']}")
            with col2:
                st.markdown(f"Status: `🟢 {doc['status'].title()}`")
                st.caption(f"Uploaded: {str(doc['upload_date'])[:10]}")
            with col3:
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button("💬 Chat", key=f"chat_doc_{doc['id']}"):
                        st.session_state['selected_doc_filter'] = doc['filename']
                        st.session_state['active_nav'] = "💬 AI Tutor"
                        st.rerun()
                with btn_col2:
                    if st.button("📝 Summary", key=f"sum_doc_{doc['id']}"):
                        st.session_state['selected_doc_id'] = doc['id']
                        st.session_state['active_nav'] = "📝 Summarize"
                        st.rerun()
                with btn_col3:
                    if st.button("🗑️", key=f"del_doc_{doc['id']}"):
                        DocumentModel.delete_document(doc['id'])
                        st.rerun()
            st.divider()
