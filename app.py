import streamlit as st
import logging

# Page Config must be first Streamlit call
st.set_page_config(
    page_title="StudyMind – AI-Powered Personal Learning OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from ui.styles import inject_custom_css
from utils.seed_demo_data import seed_demo_data_if_needed
from database.models import UserModel

# Import page views
from ui.pages.auth_view import render_auth_page
from ui.pages.dashboard_view import render_dashboard_page
from ui.pages.library_view import render_library_page
from ui.pages.tutor_view import render_tutor_page
from ui.pages.search_view import render_search_page
from ui.pages.summarize_view import render_summarize_page
from ui.pages.quiz_view import render_quiz_page
from ui.pages.flashcards_view import render_flashcards_page
from ui.pages.mock_exam_view import render_mock_exam_page
from ui.pages.study_planner_view import render_study_planner_page
from ui.pages.analytics_view import render_analytics_page
from ui.pages.weak_topics_view import render_weak_topics_page
from ui.pages.responsible_ai_view import render_responsible_ai_page
from ui.pages.settings_view import render_settings_page
from ui.pages.professor_demo_view import render_professor_demo_page

logger = logging.getLogger(__name__)

def main():
    # Inject Custom CSS
    inject_custom_css()

    # Check Authentication Gate
    user = st.session_state.get("authenticated_user")
    if not user:
        render_auth_page()
        return

    # Sidebar Header Branding
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 16px;">
            <div style="font-size: 1.6rem; font-weight: 800; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
                <span>🧠</span> <span>StudyMind</span>
            </div>
            <div style="font-size: 0.76rem; color: #818cf8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;">
                AI Personal Learning OS
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation Options
        nav_options = [
            "🏠 Dashboard",
            "📚 My Library",
            "💬 AI Tutor",
            "🔎 Semantic Search",
            "📝 Summarize",
            "🎯 Quiz Generator",
            "🃏 Flashcards",
            "🧪 Mock Exam",
            "📅 Study Planner",
            "📊 Analytics",
            "🧠 Weak Topics",
            "⚖️ Responsible AI",
            "🧪 How It Works (Viva)",
            "⚙ Settings"
        ]

        # Handle navigation state
        default_nav = st.session_state.get("active_nav", "🏠 Dashboard")
        default_idx = nav_options.index(default_nav) if default_nav in nav_options else 0

        selected_nav = st.radio(
            "Main Navigation",
            nav_options,
            index=default_idx,
            label_visibility="collapsed"
        )
        st.session_state["active_nav"] = selected_nav

        st.markdown("---")
        
        # Logged In User Profile & Logout
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 12px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="font-size: 1.4rem;">🧑‍🎓</div>
                <div>
                    <div style="font-weight: 700; font-size: 0.9rem; color: #f8fafc;">{user.get('name', 'Student')}</div>
                    <div style="font-size: 0.73rem; color: #818cf8;">{user.get('email', 'private@studymind.ai')}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">Level {user.get('level', 1)} • {user.get('xp_points', 150)} XP</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Sign Out", key="btn_logout", use_container_width=True):
            st.session_state["authenticated_user"] = None
            st.session_state["active_nav"] = "🏠 Dashboard"
            st.rerun()

    # Route to Selected Page View
    if selected_nav == "🏠 Dashboard":
        render_dashboard_page()
    elif selected_nav == "📚 My Library":
        render_library_page()
    elif selected_nav == "💬 AI Tutor":
        render_tutor_page()
    elif selected_nav == "🔎 Semantic Search":
        render_search_page()
    elif selected_nav == "📝 Summarize":
        render_summarize_page()
    elif selected_nav == "🎯 Quiz Generator":
        render_quiz_page()
    elif selected_nav == "🃏 Flashcards":
        render_flashcards_page()
    elif selected_nav == "🧪 Mock Exam":
        render_mock_exam_page()
    elif selected_nav == "📅 Study Planner":
        render_study_planner_page()
    elif selected_nav == "📊 Analytics":
        render_analytics_page()
    elif selected_nav == "🧠 Weak Topics":
        render_weak_topics_page()
    elif selected_nav == "⚖️ Responsible AI":
        render_responsible_ai_page()
    elif selected_nav == "🧪 How It Works (Viva)":
        render_professor_demo_page()
    elif selected_nav == "⚙ Settings":
        render_settings_page()

if __name__ == "__main__":
    main()
