import streamlit as st
from ui.components import UIComponents
from features.study_plan import StudyPlanFeature
from database.models import UserModel

def render_study_planner_page():
    UIComponents.render_header(
        title="Personalized AI Study Planner",
        subtitle="AI-driven study schedule tailored to your subjects, exam date, and weak topics.",
        icon="📅"
    )

    user = UserModel.get_user()

    with st.expander("⚙️ Configure Study Planner Parameters", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            subjects = st.text_input("Subjects/Courses", "Operating Systems, DBMS, Computer Networks, AI")
        with col2:
            exam_date = st.date_input("Target Exam Date")
        with col3:
            daily_hours = st.slider("Daily Study Hours", min_value=1.0, max_value=8.0, value=float(user.get("daily_hours", 2.5)), step=0.5)

        if st.button("✨ Regenerate AI Schedule", key="btn_regen_plan"):
            with st.spinner("Analyzing target exam date, daily hours & weak topics..."):
                StudyPlanFeature.generate_personalized_plan(
                    subjects=subjects,
                    exam_date=str(exam_date),
                    daily_hours=daily_hours
                )
                st.rerun()

    st.markdown("---")
    st.markdown("### 📅 Dynamic Study Schedule")

    plans = StudyPlanFeature.get_plans()
    if not plans:
        st.info("No study tasks found. Click 'Regenerate AI Schedule' above.")
        return

    # Group by date
    dates = sorted(list(set([p['plan_date'] for p in plans])))

    for d in dates:
        st.markdown(f"#### 📆 {d}")
        day_tasks = [p for p in plans if p['plan_date'] == d]
        
        for task in day_tasks:
            t_id = task['id']
            is_done = (task['status'] == 'completed')
            
            with st.container():
                col_check, col_info = st.columns([1, 11])
                with col_check:
                    checked = st.checkbox(f"Done_{t_id}", value=is_done, key=f"plan_chk_{t_id}", label_visibility="collapsed")
                    if checked != is_done:
                        StudyPlanFeature.toggle_task(t_id, task['status'])
                        st.rerun()

                with col_info:
                    st.markdown(f"**{task['time_slot']}** – **{task['title']}** (`{task['topic']}`)")
                    st.caption(f"{task['task_description']}")
            st.divider()
