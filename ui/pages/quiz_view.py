import time
import streamlit as st
from ui.components import UIComponents
from database.models import DocumentModel
from features.quiz import QuizFeature

def render_quiz_page():
    UIComponents.render_header(
        title="Quiz Generator & Adaptive Learning",
        subtitle="Generate dynamic AI quizzes from study material and test your understanding.",
        icon="🎯"
    )

    user = st.session_state.get("authenticated_user")
    user_id = user["id"] if user else 1
    docs = DocumentModel.get_all_documents(user_id=user_id)

    if not docs:
        st.info("No study materials uploaded yet. Go to **My Library (📚)** to upload your notes or PDFs to generate accurate quizzes!")
        return

    doc_options = {d["filename"]: d["id"] for d in docs}
    doc_names = list(doc_options.keys())
    
    col_t, col_d, col_q, col_n = st.columns(4)
    with col_t:
        selected_doc_name = st.selectbox("Select Study Document", doc_names)
        selected_doc_id = doc_options[selected_doc_name]
    with col_d:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
    with col_q:
        q_type = st.selectbox("Question Type", ["MCQ", "True-False", "Short Answer", "Mixed"])
    with col_n:
        num_questions = st.select_slider("Questions", [3, 5, 10], value=5)

    is_adaptive = st.toggle("🧠 Enable Adaptive Difficulty Mode", value=True, help="Difficulty dynamically adjusts based on your live accuracy.")

    if st.button("🚀 Generate Quiz", key="btn_gen_quiz", use_container_width=True):
        diff_bar_map = {
            "Easy": "███░░░░░░░ 30%",
            "Medium": "██████░░░░ 60%",
            "Hard": "█████████░ 90%"
        }
        initial_diff_bar = diff_bar_map.get(difficulty, "██████░░░░ 60%")

        with st.spinner(f"Analyzing '{selected_doc_name}' context & generating ground-truth quiz questions..."):
            questions = QuizFeature.generate_quiz(
                topic=selected_doc_name,
                doc_id=selected_doc_id,
                num_questions=num_questions,
                difficulty=difficulty,
                question_type=q_type,
                user_id=user_id
            )
            st.session_state["active_quiz"] = {
                "topic": selected_doc_name,
                "doc_id": selected_doc_id,
                "difficulty": difficulty,
                "question_type": q_type,
                "questions": questions,
                "start_time": time.time(),
                "current_diff": difficulty,
                "consec_correct": 0,
                "consec_wrong": 0,
                "diff_bar": initial_diff_bar
            }
            st.session_state["quiz_submitted"] = False
            st.session_state["quiz_answers"] = {}
            st.rerun()

    active_quiz = st.session_state.get("active_quiz")
    if not active_quiz:
        st.info("Select quiz parameters above and click 'Generate Quiz' to begin.")
        return

    st.markdown("---")
    
    if is_adaptive:
        st.markdown(f"**Adaptive Quiz Engine Active** | Live Difficulty Level: `{active_quiz['current_diff']}`")
        st.caption(f"Difficulty Bar: `{active_quiz['diff_bar']}`")

    questions = active_quiz["questions"]
    user_answers = st.session_state.get("quiz_answers", {})
    is_submitted = st.session_state.get("quiz_submitted", False)

    for idx, q in enumerate(questions):
        q_id = q.get("id", idx + 1)
        st.markdown(f"#### Question {idx + 1} of {len(questions)}")
        st.markdown(f"**{q['question']}**")

        options = q.get("options", ["True", "False"])
        
        if not is_submitted:
            ans = st.radio(
                f"Select your answer for Q{idx+1}:",
                options,
                key=f"q_ans_{q_id}",
                index=None
            )
            if ans:
                user_answers[q_id] = ans
                st.session_state["quiz_answers"] = user_answers
        else:
            selected_ans = user_answers.get(q_id, "Not Answered")
            correct_ans = q.get("correct_answer")
            is_correct = (selected_ans == correct_ans)

            if is_correct:
                st.success(f"✅ **Correct!** Your Answer: `{selected_ans}`")
            else:
                st.error(f"❌ **Incorrect.** Your Answer: `{selected_ans}` | Correct Answer: `{correct_ans}`")

            st.markdown(f"**Explanation:** {q.get('explanation', '')}")
            if q.get("source_snippet"):
                st.caption(f"📄 Source Snippet: {q.get('source_snippet')}")

        st.divider()

    if not is_submitted:
        if st.button("📥 Submit Quiz", key="btn_submit_quiz"):
            st.session_state["quiz_submitted"] = True
            time_taken = int(time.time() - active_quiz["start_time"])

            # Compute score
            score = 0
            for idx, q in enumerate(questions):
                q_id = q.get("id", idx + 1)
                u_ans = user_answers.get(q_id)
                c_ans = q.get("correct_answer")
                if u_ans and u_ans == c_ans:
                    score += 1

                # Update adaptive difficulty
                if is_adaptive:
                    new_diff, diff_bar, cc, cw = QuizFeature.calculate_adaptive_difficulty(
                        current_difficulty=active_quiz["current_diff"],
                        is_correct=(u_ans == c_ans),
                        consecutive_correct=active_quiz["consec_correct"],
                        consecutive_wrong=active_quiz["consec_wrong"]
                    )
                    active_quiz["current_diff"] = new_diff
                    active_quiz["diff_bar"] = diff_bar
                    active_quiz["consec_correct"] = cc
                    active_quiz["consec_wrong"] = cw

            QuizFeature.save_quiz_results(
                topic=active_quiz["topic"],
                difficulty=active_quiz["difficulty"],
                question_type=active_quiz["question_type"],
                score=score,
                max_score=len(questions),
                time_taken_sec=time_taken,
                details=questions,
                user_id=user_id
            )
            st.rerun()
    else:
        st.balloons()
        st.success("Quiz completed and score saved to your persistent learning history!")
