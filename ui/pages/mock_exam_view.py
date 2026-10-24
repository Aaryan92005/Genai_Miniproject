import time
import streamlit as st
from ui.components import UIComponents
from features.mock_exam import MockExamFeature

def render_mock_exam_page():
    UIComponents.render_header(
        title="Mock Examination",
        subtitle="Test your knowledge under university examination conditions.",
        icon="🧪"
    )

    col_subj, col_top, col_q, col_d = st.columns(4)
    with col_subj:
        subject = st.selectbox("Subject", ["Computer Science", "Software Engineering", "AI & ML"])
    with col_top:
        topics = st.text_input("Exam Topics", "Operating Systems, DBMS Normalization")
    with col_q:
        num_q = st.select_slider("Questions", [5, 10, 15], value=10)
    with col_d:
        difficulty = st.selectbox("Exam Difficulty", ["Medium", "Hard"])

    if st.button("🚀 Start Distraction-Free Exam", key="btn_start_exam"):
        with st.spinner("Generating university exam paper from vector knowledge base..."):
            exam_data = MockExamFeature.generate_exam(
                subject=subject,
                topics=topics,
                num_questions=num_q,
                difficulty=difficulty
            )
            st.session_state["active_exam"] = exam_data
            st.session_state["exam_start_time"] = time.time()
            st.session_state["exam_user_answers"] = {}
            st.session_state["exam_submitted"] = False
            st.rerun()

    active_exam = st.session_state.get("active_exam")
    if not active_exam:
        st.info("Configure your exam parameters above and click 'Start Distraction-Free Exam'.")
        return

    st.markdown("---")
    
    # Exam Header & Timer
    is_submitted = st.session_state.get("exam_submitted", False)
    start_time = st.session_state.get("exam_start_time", time.time())
    elapsed_sec = int(time.time() - start_time)
    remaining_sec = max(0, (active_exam["duration_minutes"] * 60) - elapsed_sec)
    rem_min = remaining_sec // 60
    rem_s = remaining_sec % 60

    col_h, col_t = st.columns([3, 1])
    with col_h:
        st.markdown(f"### 📝 {active_exam['exam_title']}")
        st.caption(f"Topics: `{active_exam['topics']}` | Total Questions: {len(active_exam['questions'])}")
    with col_t:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); padding: 10px; border-radius: 10px; text-align: center;">
            <div style="font-size: 0.75rem; color: #fca5a5; font-weight: 700; text-transform: uppercase;">TIME REMAINING</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #ef4444;">{rem_min:02d}:{rem_s:02d}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    questions = active_exam["questions"]
    user_answers = st.session_state.get("exam_user_answers", {})

    if not is_submitted:
        for idx, q in enumerate(questions):
            q_id = q.get("id", idx + 1)
            st.markdown(f"**Question {idx + 1}: {q['question']}**")
            options = q.get("options", ["Option A", "Option B", "Option C", "Option D"])
            
            ans = st.radio(
                f"Select answer for Q{idx+1}:",
                options,
                key=f"exam_q_{q_id}",
                index=None
            )
            if ans:
                user_answers[q_id] = ans
                st.session_state["exam_user_answers"] = user_answers
            st.divider()

        if st.button("📥 Submit Exam Paper", key="btn_submit_exam"):
            st.session_state["exam_submitted"] = True
            report = MockExamFeature.evaluate_exam(active_exam, user_answers, elapsed_sec)
            st.session_state["exam_report"] = report
            st.rerun()

    else:
        report = st.session_state.get("exam_report")
        if report:
            st.markdown("## 📊 Official Exam Evaluation Report")
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                UIComponents.render_metric_card("🎯", "Exam Score", f"{report['percentage']}%", f"{report['score']} / {report['max_score']} Correct")
            with col_s2:
                UIComponents.render_metric_card("⏱️", "Time Spent", f"{report['time_taken_sec'] // 60}m {report['time_taken_sec'] % 60}s", f"Limit: {active_exam['duration_minutes']} mins")
            with col_s3:
                UIComponents.render_metric_card("🎖️", "XP Awarded", f"+{report['score'] * 20} XP", "Added to Rank")

            st.markdown(f'<div class="sm-card-gradient">{report["feedback"]}</div>', unsafe_allow_html=True)

            col_str, col_wk = st.columns(2)
            with col_str:
                st.markdown("### 🟢 Strong Topics")
                for t in report.get("strong_topics", ["Core Concepts"]):
                    st.success(f"✓ {t}")
            with col_wk:
                st.markdown("### 🔴 Weak Topics (Requires Revision)")
                for t in report.get("weak_topics", ["Edge Cases"]):
                    st.error(f"⚠️ {t}")

            if st.button("🔄 Take Another Exam"):
                st.session_state["active_exam"] = None
                st.session_state["exam_submitted"] = False
                st.rerun()
