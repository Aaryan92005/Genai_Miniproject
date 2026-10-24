import streamlit as st
from ui.components import UIComponents
from database.models import DocumentModel
from features.chat import ChatFeature

def render_tutor_page():
    UIComponents.render_header(
        title="AI Tutor",
        subtitle="Ask questions, explore tutoring modes, and get grounded explanations with source citations.",
        icon="💬"
    )

    user = st.session_state.get("authenticated_user", {})
    user_id = user.get("id", 1)

    docs = DocumentModel.get_all_documents(user_id=user_id)
    doc_options = {"All My Materials": None}
    if docs:
        for d in docs:
            doc_options[d["filename"]] = d["id"]

    # Control Bar: Scope, Modes and Explanation Levels
    col_doc, col_mode, col_lvl, col_k, col_cls = st.columns([2, 2, 2, 1, 1])

    with col_doc:
        selected_doc_label = st.selectbox("Focus Material", list(doc_options.keys()))
        selected_doc_id = doc_options[selected_doc_label]

    with col_mode:
        tutor_mode = st.radio(
            "Tutoring Mode",
            ["Explain", "Teach", "Exam", "Socratic", "Simple"],
            horizontal=True,
            index=0,
            help="Select how StudyMind teaches you."
        )

    with col_lvl:
        explanation_level = st.select_slider(
            "Explanation Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )

    with col_k:
        top_k = st.number_input("Top K", min_value=1, max_value=10, value=3)

    with col_cls:
        st.write("")
        st.write("")
        if st.button("🧹 Clear", help="Reset Chat Thread", use_container_width=True):
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": "Hello! I am StudyMind, your personal AI tutor. Ask me anything about your uploaded study materials!",
                    "sources": [],
                    "transparency": None
                }
            ]
            st.rerun()

    st.markdown("---")

    # Chat Session History state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hello! I am StudyMind, your personal AI tutor. Ask me anything about your uploaded study materials!",
                "sources": [],
                "transparency": None
            }
        ]

    # Render Chat History
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="sm-chat-user"><b>🧑‍🎓 Student:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="sm-chat-ai"><b>🧠 StudyMind AI Tutor:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
            if msg.get("sources"):
                UIComponents.render_source_chips(msg["sources"])
            if msg.get("transparency"):
                UIComponents.render_transparency_accordion(msg["transparency"])

    # User Input Field
    user_input = st.chat_input(f"Ask AI Tutor about {selected_doc_label}...")

    if user_input:
        # Append User Message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner("Searching knowledge base & constructing grounded answer..."):
            res = ChatFeature.process_user_query(
                question=user_input,
                mode=tutor_mode,
                level=explanation_level,
                top_k=top_k,
                user_id=user_id,
                doc_id=selected_doc_id
            )

        if res:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": res["answer"],
                "sources": res.get("sources", []),
                "transparency": res.get("transparency")
            })

        st.rerun()
