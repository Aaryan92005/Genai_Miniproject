import streamlit as st
from ui.components import UIComponents
from database.models import DocumentModel
from features.flashcards import FlashcardFeature

def render_flashcards_page():
    UIComponents.render_header(
        title="Smart Flashcards",
        subtitle="Master high-yield concepts using active recall and spaced repetition.",
        icon="🃏"
    )

    user = st.session_state.get("authenticated_user")
    user_id = user["id"] if user else 1

    docs = DocumentModel.get_all_documents(user_id=user_id)
    if not docs:
        st.info("No study materials uploaded yet. Go to **My Library (📚)** to upload your notes or PDFs and generate smart flashcards!")
        return

    doc_options = {d["filename"]: d["id"] for d in docs}
    doc_names = list(doc_options.keys())
    
    selected_doc_name = st.selectbox("Select Study Material for Flashcard Generation", doc_names)
    selected_doc_id = doc_options[selected_doc_name]

    if st.button("✨ Generate AI Flashcard Deck", key="btn_gen_cards", use_container_width=True):
        with st.spinner(f"Synthesizing concept flashcards for '{selected_doc_name}'..."):
            FlashcardFeature.generate_cards(topic=selected_doc_name, doc_id=selected_doc_id, num_cards=6, user_id=user_id)
            st.success(f"Generated new Flashcard deck for '{selected_doc_name}'!")
            st.rerun()

    cards = FlashcardFeature.get_cards_for_topic(topic=selected_doc_name, user_id=user_id)
    if not cards:
        cards = FlashcardFeature.get_cards_for_topic(topic="All Topics", user_id=user_id)

    # Index management in session state
    if "card_idx" not in st.session_state:
        st.session_state["card_idx"] = 0
    if "card_flipped" not in st.session_state:
        st.session_state["card_flipped"] = False

    curr_idx = min(st.session_state["card_idx"], len(cards) - 1)
    card = cards[curr_idx]

    st.markdown("---")
    st.caption(f"Card {curr_idx + 1} of {len(cards)} | Topic: `{card['topic']}` | Mastery: `{card.get('mastery_score', 0)}%`")

    # Render Flashcard Container
    is_flipped = st.session_state["card_flipped"]

    if not is_flipped:
        st.markdown(f"""
        <div class="sm-card" style="height: 240px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; border: 2px solid #6366f1;">
            <div style="font-size: 0.85rem; color: #818cf8; text-transform: uppercase; font-weight: 700; margin-bottom: 8px;">QUESTION</div>
            <h3 style="color: #f8fafc; font-size: 1.35rem; margin: 0 20px;">{card['question']}</h3>
            <div style="margin-top: 20px; font-size: 0.82rem; color: #64748b;">(Click 'Flip Card' below to reveal answer)</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="sm-card-gradient" style="height: 240px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
            <div style="font-size: 0.85rem; color: #a855f7; text-transform: uppercase; font-weight: 700; margin-bottom: 8px;">ANSWER</div>
            <p style="color: #f8fafc; font-size: 1.15rem; line-height: 1.5; margin: 0 20px;">{card['answer']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Card Actions
    col_flip, col_knew, col_again = st.columns(3)

    with col_flip:
        if st.button("🔄 Flip Card", key="btn_flip"):
            st.session_state["card_flipped"] = not is_flipped
            st.rerun()

    with col_knew:
        if st.button("✅ I Know This (+5 XP)", key="btn_knew"):
            FlashcardFeature.record_review(card["id"], knew_it=True)
            st.session_state["card_flipped"] = False
            st.session_state["card_idx"] = (curr_idx + 1) % len(cards)
            st.rerun()

    with col_again:
        if st.button("↻ Review Again", key="btn_again"):
            FlashcardFeature.record_review(card["id"], knew_it=False)
            st.session_state["card_flipped"] = False
            st.session_state["card_idx"] = (curr_idx + 1) % len(cards)
            st.rerun()

    # Navigation Buttons
    col_prev, _, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("← Previous", key="btn_prev_card"):
            st.session_state["card_flipped"] = False
            st.session_state["card_idx"] = max(0, curr_idx - 1)
            st.rerun()
    with col_next:
        if st.button("Next →", key="btn_next_card"):
            st.session_state["card_flipped"] = False
            st.session_state["card_idx"] = (curr_idx + 1) % len(cards)
            st.rerun()
