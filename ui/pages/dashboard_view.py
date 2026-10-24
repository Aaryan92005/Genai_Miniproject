import streamlit as st
from ui.components import UIComponents
from features.analytics import AnalyticsFeature
from features.study_plan import StudyPlanFeature
from database.models import UserModel, DocumentModel, QuizModel, WeakTopicModel

def render_dashboard_page():
    user = st.session_state.get("authenticated_user", {})
    user_id = user.get("id", 1)
    db_user = UserModel.get_user(user_id=user_id)

    UIComponents.render_header(
        title=f"Welcome back, {db_user.get('name', 'Student')} 👋",
        subtitle="Here is your personal Generative AI learning overview, study metrics, and navigation hub.",
        icon="🚀",
        badge="DASHBOARD OVERVIEW"
    )

    metrics = AnalyticsFeature.get_dashboard_metrics(user_id=user_id)

    # 4 Top Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        UIComponents.render_metric_card("📚", "Knowledge Base", f"{metrics['doc_count']} Docs", "Indexed Study Materials")
    with col2:
        UIComponents.render_metric_card("🔥", "Study Streak", f"{metrics['streak']} Days", "Continuous Active Learning")
    with col3:
        UIComponents.render_metric_card("🎯", "Quiz Performance", f"{metrics['quiz_accuracy']}%", "Average Mastery Accuracy")
    with col4:
        UIComponents.render_metric_card("⏱️", "Total Focus Time", f"{metrics['study_hours']} hrs", "Logged Learning Sessions")

    st.markdown("---")

    # Interactive Quick Launch Navigation Hub
    st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 14px;'>⚡ Quick Launch Study Hub</h3>", unsafe_allow_html=True)
    
    # 4x2 Grid of Feature Launch Buttons
    gcol1, gcol2, gcol3, gcol4 = st.columns(4)
    
    with gcol1:
        with st.container():
            st.markdown("#### 💬 AI Tutor")
            st.caption("Ask questions & get grounded answers with source citations.")
            if st.button("🚀 Open AI Tutor", key="dash_nav_tutor", use_container_width=True):
                st.session_state["active_nav"] = "💬 AI Tutor"
                st.rerun()

    with gcol2:
        with st.container():
            st.markdown("#### 📚 My Library")
            st.caption("Upload & manage PDFs, notes, and textbook chapters.")
            if st.button("🚀 Open Library", key="dash_nav_lib", use_container_width=True):
                st.session_state["active_nav"] = "📚 My Library"
                st.rerun()

    with gcol3:
        with st.container():
            st.markdown("#### 🔎 Semantic Search")
            st.caption("Vector similarity search across your uploaded documents.")
            if st.button("🚀 Open Search", key="dash_nav_search", use_container_width=True):
                st.session_state["active_nav"] = "🔎 Semantic Search"
                st.rerun()

    with gcol4:
        with st.container():
            st.markdown("#### 📝 Summarizer")
            st.caption("Generate executive, medium, or detailed study guides.")
            if st.button("🚀 Open Summarizer", key="dash_nav_sum", use_container_width=True):
                st.session_state["active_nav"] = "📝 Summarize"
                st.rerun()

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    gcol5, gcol6, gcol7, gcol8 = st.columns(4)

    with gcol5:
        with st.container():
            st.markdown("#### 🎯 Quiz Generator")
            st.caption("Generate custom MCQs & test your conceptual accuracy.")
            if st.button("🚀 Start Quiz", key="dash_nav_quiz", use_container_width=True):
                st.session_state["active_nav"] = "🎯 Quiz Generator"
                st.rerun()

    with gcol6:
        with st.container():
            st.markdown("#### 🃏 Flashcards")
            st.caption("Revise key terms with spaced repetition cards.")
            if st.button("🚀 Study Flashcards", key="dash_nav_flash", use_container_width=True):
                st.session_state["active_nav"] = "🃏 Flashcards"
                st.rerun()

    with gcol7:
        with st.container():
            st.markdown("#### 🧪 Mock Exam")
            st.caption("Simulate timed university exam questions under pressure.")
            if st.button("🚀 Take Mock Exam", key="dash_nav_mock", use_container_width=True):
                st.session_state["active_nav"] = "🧪 Mock Exam"
                st.rerun()

    with gcol8:
        with st.container():
            st.markdown("#### 📅 Study Planner")
            st.caption("Personalized daily AI study schedule and task tracker.")
            if st.button("🚀 View Schedule", key="dash_nav_plan", use_container_width=True):
                st.session_state["active_nav"] = "📅 Study Planner"
                st.rerun()

    st.markdown("---")

    # AI Insight Card & Student Level & Rank
    col_left, col_right = st.columns([1.65, 1])

    with col_left:
        st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 12px;'>🧠 Dynamic AI Learning Insight</h3>", unsafe_allow_html=True)
        
        # Compute dynamic insight from database
        user_docs = DocumentModel.get_all_documents(user_id=user_id)
        weak_topics = WeakTopicModel.get_weak_topics(user_id=user_id)

        if not user_docs:
            insight_title = "Welcome to StudyMind AI!"
            insight_text = (
                "You haven't uploaded any study materials yet. Head over to **My Library (📚)** "
                "to upload your course PDFs, lecture notes, or syllabus. Once uploaded, StudyMind will generate "
                "personalized AI flashcards, quizzes, and RAG tutor answers!"
            )
        elif weak_topics:
            top_weak = weak_topics[0]
            insight_title = f"Focus Area: {top_weak['topic']}"
            insight_text = (
                f"Based on your recent quiz attempts, your lowest accuracy topic is **{top_weak['topic']} "
                f"({top_weak['accuracy_percentage']}% accuracy)**. "
                "We recommend using **AI Tutor (💬)** or **Flashcards (🃏)** to practice this topic before your upcoming exam."
            )
        else:
            doc_names = ", ".join([f"`{d['filename']}`" for d in user_docs[:3]])
            insight_title = "Library Ready for Learning!"
            insight_text = (
                f"You have **{len(user_docs)} study materials** indexed ({doc_names}). "
                "Try taking a practice quiz in **Quiz Generator (🎯)** or chatting with your **AI Tutor (💬)** to test your knowledge!"
            )

        UIComponents.render_ai_insight_card(
            title=insight_title,
            content=insight_text
        )

    with col_right:
        st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 12px;'>🏆 Student Rank</h3>", unsafe_allow_html=True)
        level = metrics['level']
        xp = metrics['xp_points']
        next_xp = max(0, (level * 100) - xp)
        st.markdown(f"""
        <div class="sm-card" style="text-align: center; padding: 24px; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: rgba(168, 85, 247, 0.15); border-radius: 50%; filter: blur(20px);"></div>
            <div style="font-size: 2.8rem; margin-bottom: 8px;">🎖️</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.01em;">Level {level} – Knowledge Seeker</div>
            <div style="font-size: 0.95rem; color: #c084fc; font-weight: 700; margin-top: 4px;">{xp} XP Earned</div>
            <div style="margin-top: 14px; background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.06); font-size: 0.8rem; color: #94a3b8;">
                ⚡ <b>{next_xp} XP</b> needed for Level {level + 1}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Today's Study Plan Tasks
    st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 14px;'>📅 Today's Study Schedule</h3>", unsafe_allow_html=True)
    plans = StudyPlanFeature.get_plans()

    if not plans:
        st.info("No study tasks scheduled for today. Generate a personalized plan in Study Planner!")
    else:
        for task in plans[:4]:
            task_id = task['id']
            is_done = task['status'] == 'completed'
            label = f"**{task['time_slot']}** — {task['title']} (`{task['topic']}`)"
            
            checked = st.checkbox(label, value=is_done, key=f"dash_task_{task_id}")
            if checked != is_done:
                StudyPlanFeature.toggle_task(task_id, task['status'])
                st.rerun()
