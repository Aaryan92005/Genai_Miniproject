import streamlit as st
from ui.components import UIComponents
from database.models import DocumentModel
from features.summaries import SummaryFeature

def render_summarize_page():
    UIComponents.render_header(
        title="Document Summarizer",
        subtitle="Extract high-yield executive summaries, key concepts, formulas, and exam questions.",
        icon="📝"
    )

    user = st.session_state.get("authenticated_user")
    user_id = user["id"] if user else 1
    docs = DocumentModel.get_all_documents(user_id=user_id)
    if not docs:
        st.info("No documents uploaded yet. Go to 'My Library' to index study files.")
        return

    doc_options = {d["filename"]: d["id"] for d in docs}
    
    # Pre-select if forwarded from library
    default_idx = 0
    if "selected_doc_id" in st.session_state:
        for idx, (name, d_id) in enumerate(doc_options.items()):
            if d_id == st.session_state["selected_doc_id"]:
                default_idx = idx
                break

    selected_doc_name = st.selectbox("Select Document to Summarize", list(doc_options.keys()), index=default_idx)
    selected_doc_id = doc_options[selected_doc_name]

    depth = st.radio("Summary Depth", ["Short", "Medium", "Detailed"], horizontal=True, index=1)

    cache_key = f"summary_cache_{selected_doc_id}_{depth}"

    col_btn1, col_btn2 = st.columns([1.5, 1])
    with col_btn1:
        if st.button("✨ Generate AI Summary", key="btn_gen_summary", use_container_width=True):
            with st.spinner(f"Synthesizing '{depth}' academic summary..."):
                summary_md = SummaryFeature.generate_summary(selected_doc_id, depth=depth)
                st.session_state[cache_key] = summary_md

    # Display Summary if available
    cached_summary = st.session_state.get(cache_key)
    if cached_summary:
        st.markdown("---")
        
        # Action Toolbar
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.markdown(f"<span style='color: #c084fc; font-weight: 700; font-size: 0.9rem;'>📄 AI Summary — {selected_doc_name} ({depth} Depth)</span>", unsafe_allow_html=True)
        with col_t2:
            st.download_button(
                label="📥 Download (.md)",
                data=cached_summary,
                file_name=f"{selected_doc_name}_summary_{depth.lower()}.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.markdown(f'<div class="sm-card" style="margin-top: 10px;">{cached_summary}</div>', unsafe_allow_html=True)
