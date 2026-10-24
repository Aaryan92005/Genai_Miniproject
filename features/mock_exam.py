import logging
from features.quiz import QuizFeature
from database.models import QuizModel

logger = logging.getLogger(__name__)

class MockExamFeature:
    @classmethod
    def generate_exam(cls, subject="Computer Science", topics="Operating Systems, DBMS", num_questions=10, difficulty="Medium"):
        """Generates a full timed mock exam."""
        questions = QuizFeature.generate_quiz(
            topic=topics,
            num_questions=num_questions,
            difficulty=difficulty,
            question_type="Mixed"
        )
        return {
            "exam_title": f"{subject} Final Mock Examination",
            "subject": subject,
            "topics": topics,
            "difficulty": difficulty,
            "duration_minutes": max(10, num_questions * 2),
            "questions": questions
        }

    @classmethod
    def evaluate_exam(cls, exam_data, user_answers, time_taken_sec):
        """
        Evaluates submitted mock exam answers, computes percentage score,
        breakdown of strong vs weak topics, and AI feedback.
        """
        questions = exam_data.get("questions", [])
        total_questions = len(questions)
        correct_count = 0
        details = []
        topic_scores = {}

        for idx, q in enumerate(questions):
            q_id = q.get("id", idx + 1)
            correct_ans = str(q.get("correct_answer", "")).strip()
            user_ans = str(user_answers.get(q_id, "")).strip()
            
            is_correct = (user_ans.lower() == correct_ans.lower()) or (correct_ans.lower() in user_ans.lower() and len(user_ans) > 2)
            if is_correct:
                correct_count += 1
                
            q_topic = q.get("topic", exam_data.get("subject", "General"))
            if q_topic not in topic_scores:
                topic_scores[q_topic] = {"correct": 0, "total": 0}
            topic_scores[q_topic]["total"] += 1
            if is_correct:
                topic_scores[q_topic]["correct"] += 1

            details.append({
                "question_id": q_id,
                "question": q.get("question"),
                "user_answer": user_ans,
                "correct_answer": correct_ans,
                "is_correct": is_correct,
                "explanation": q.get("explanation", ""),
                "source_snippet": q.get("source_snippet", "")
            })

        percentage = round((correct_count / total_questions * 100.0) if total_questions > 0 else 0.0, 1)

        # Categorize Strong & Weak Topics
        strong_topics = []
        weak_topics = []
        for t, sc in topic_scores.items():
            acc = (sc["correct"] / sc["total"]) * 100.0 if sc["total"] > 0 else 0
            if acc >= 70:
                strong_topics.append(f"{t} ({round(acc)}%)")
            else:
                weak_topics.append(f"{t} ({round(acc)}%)")

        # Save to DB
        QuizModel.save_quiz_attempt(
            topic=f"Mock Exam: {exam_data['subject']}",
            difficulty=exam_data['difficulty'],
            question_type="Mock Exam",
            score=correct_count,
            max_score=total_questions,
            time_taken_sec=time_taken_sec,
            details=details
        )

        # AI Feedback Generation
        if percentage >= 85:
            feedback = f"🌟 Outstanding Performance! You scored {percentage}%. You showed deep conceptual clarity in {', '.join(strong_topics) if strong_topics else 'all sections'}."
        elif percentage >= 60:
            feedback = f"👍 Good Job! You passed with {percentage}%. Strong in {', '.join(strong_topics) if strong_topics else 'core topics'}, but need to revise {', '.join(weak_topics) if weak_topics else 'edge cases'} before final exam."
        else:
            feedback = f"⚠️ Needs Revision. You scored {percentage}%. Key weak areas identified: {', '.join(weak_topics) if weak_topics else 'multiple topics'}. Use 'Fix My Weakness' mode to target these topics."

        return {
            "score": correct_count,
            "max_score": total_questions,
            "percentage": percentage,
            "time_taken_sec": time_taken_sec,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "feedback": feedback,
            "details": details
        }
