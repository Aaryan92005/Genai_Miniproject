import json
import hashlib
from datetime import datetime
from database.db import execute_query, get_connection

def hash_password(password: str) -> str:
    """Computes SHA-256 salted hash of password."""
    return hashlib.sha256((password + "studymind_salt_2026").encode('utf-8')).hexdigest()

class UserModel:
    @staticmethod
    def register(name, email, password):
        email = email.strip().lower()
        existing = execute_query("SELECT * FROM users WHERE LOWER(email) = ?", (email,), fetch_all=False)
        if existing:
            return None, "An account with this email already exists."

        pwd_hash = hash_password(password)
        today = datetime.now().strftime('%Y-%m-%d')
        user_id = execute_query('''
            INSERT INTO users (name, email, password_hash, target_exam_date, daily_hours, level, xp_points, streak_count, last_active_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, pwd_hash, '2026-10-15', 2.5, 1, 150, 1, today), fetch_all=False)

        user = UserModel.get_user_by_id(user_id)
        return user, "Registration successful!"

    @staticmethod
    def authenticate(email, password):
        email = email.strip().lower()
        pwd_hash = hash_password(password)
        user = execute_query("SELECT * FROM users WHERE LOWER(email) = ? AND password_hash = ?", (email, pwd_hash), fetch_all=False)
        if not user:
            return None, "Invalid email or password."
        return user, "Authentication successful."

    @staticmethod
    def get_user_by_id(user_id):
        res = execute_query("SELECT * FROM users WHERE id = ?", (user_id,), fetch_all=False)
        return res

    @staticmethod
    def get_user(user_id=1):
        res = execute_query("SELECT * FROM users WHERE id = ?", (user_id,), fetch_all=False)
        if not res:
            res = execute_query("SELECT * FROM users ORDER BY id ASC LIMIT 1", fetch_all=False)
        if not res:
            return {
                "id": 1, "name": "Student", "email": "student@studymind.ai",
                "target_exam_date": "2026-10-15", "daily_hours": 2.5,
                "level": 1, "xp_points": 150, "streak_count": 3, "last_active_date": datetime.now().strftime('%Y-%m-%d')
            }
        return res

    @staticmethod
    def update_user_profile(user_id, name, target_exam_date, daily_hours):
        execute_query(
            "UPDATE users SET name = ?, target_exam_date = ?, daily_hours = ? WHERE id = ?",
            (name, target_exam_date, daily_hours, user_id),
            fetch_all=False
        )

    @staticmethod
    def add_xp(user_id, points):
        user = UserModel.get_user_by_id(user_id) or UserModel.get_user(1)
        u_id = user.get("id", user_id)
        new_xp = user.get("xp_points", 0) + points
        new_level = max(1, new_xp // 100 + 1)
        execute_query(
            "UPDATE users SET xp_points = ?, level = ? WHERE id = ?",
            (new_xp, new_level, u_id),
            fetch_all=False
        )
        return new_xp, new_level

class DocumentModel:
    @staticmethod
    def add_document(filename, file_type, file_size, page_count, chunk_count, topics=None, summary=None, user_id=1):
        topics_json = json.dumps(topics or [])
        summary_json = json.dumps(summary or {})
        doc_id = execute_query('''
            INSERT INTO documents (user_id, filename, file_type, file_size, page_count, chunk_count, topics_json, summary_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, filename, file_type, file_size, page_count, chunk_count, topics_json, summary_json), fetch_all=False)
        return doc_id

    @staticmethod
    def get_all_documents(user_id=1):
        docs = execute_query("SELECT * FROM documents WHERE user_id = ? ORDER BY upload_date DESC", (user_id,))
        for d in docs:
            d['topics'] = json.loads(d.get('topics_json', '[]') or '[]')
            d['summary'] = json.loads(d.get('summary_json', '{}') or '{}')
        return docs

    @staticmethod
    def get_document_by_id(doc_id):
        doc = execute_query("SELECT * FROM documents WHERE id = ?", (doc_id,), fetch_all=False)
        if doc:
            doc['topics'] = json.loads(doc.get('topics_json', '[]') or '[]')
            doc['summary'] = json.loads(doc.get('summary_json', '{}') or '{}')
        return doc

    @staticmethod
    def delete_document(doc_id):
        execute_query("DELETE FROM document_chunks WHERE doc_id = ?", (doc_id,), fetch_all=False)
        execute_query("DELETE FROM documents WHERE id = ?", (doc_id,), fetch_all=False)
        try:
            from core.vector_store import global_vector_store
            global_vector_store.delete_document(doc_id)
        except Exception as e:
            pass

    @staticmethod
    def add_chunks(doc_id, chunks, user_id=1):
        conn = get_connection()
        cursor = conn.cursor()
        for c in chunks:
            cursor.execute('''
                INSERT INTO document_chunks (doc_id, user_id, chunk_index, page_number, content)
                VALUES (?, ?, ?, ?, ?)
            ''', (doc_id, user_id, c['chunk_index'], c.get('page_number', 1), c['content']))
        conn.commit()
        conn.close()

    @staticmethod
    def get_chunks_for_doc(doc_id):
        return execute_query("SELECT * FROM document_chunks WHERE doc_id = ? ORDER BY chunk_index ASC", (doc_id,))

    @staticmethod
    def get_all_chunks(user_id=1):
        return execute_query('''
            SELECT c.*, d.filename FROM document_chunks c
            JOIN documents d ON c.doc_id = d.id
            WHERE c.user_id = ?
        ''', (user_id,))

class QuizModel:
    @staticmethod
    def save_quiz_attempt(user_id, topic, difficulty, question_type, score, max_score, time_taken_sec, details):
        percentage = round((score / max_score * 100.0) if max_score > 0 else 0.0, 1)
        details_json = json.dumps(details)
        attempt_id = execute_query('''
            INSERT INTO quiz_attempts (user_id, topic, difficulty, question_type, score, max_score, percentage, time_taken_sec, details_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, topic, difficulty, question_type, score, max_score, percentage, time_taken_sec, details_json), fetch_all=False)
        
        UserModel.add_xp(user_id, score * 15)
        WeakTopicModel.update_topic_performance(user_id, topic, score, max_score)
        return attempt_id

    @staticmethod
    def get_all_attempts(user_id=1):
        attempts = execute_query("SELECT * FROM quiz_attempts WHERE user_id = ? ORDER BY attempted_at DESC", (user_id,))
        for a in attempts:
            a['details'] = json.loads(a.get('details_json', '[]') or '[]')
        return attempts

    @staticmethod
    def get_overall_accuracy(user_id=1):
        res = execute_query("SELECT AVG(percentage) as avg_acc, COUNT(*) as count FROM quiz_attempts WHERE user_id = ?", (user_id,), fetch_all=False)
        if not res or res.get('count', 0) == 0:
            return 82.5
        return round(res['avg_acc'] or 82.5, 1)

class FlashcardModel:
    @staticmethod
    def add_flashcards(cards, user_id=1):
        conn = get_connection()
        cursor = conn.cursor()
        for c in cards:
            cursor.execute('''
                INSERT INTO flashcards (user_id, doc_id, topic, question, answer, difficulty)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, c.get('doc_id'), c['topic'], c['question'], c['answer'], c.get('difficulty', 'Medium')))
        conn.commit()
        conn.close()

    @staticmethod
    def get_cards(topic=None, user_id=1):
        if topic and topic != "All Topics":
            return execute_query("SELECT * FROM flashcards WHERE user_id = ? AND topic = ? ORDER BY id ASC", (user_id, topic))
        return execute_query("SELECT * FROM flashcards WHERE user_id = ? ORDER BY id ASC", (user_id,))

    @staticmethod
    def update_mastery(card_id, knew_it=True, user_id=1):
        card = execute_query("SELECT * FROM flashcards WHERE id = ?", (card_id,), fetch_all=False)
        if card:
            new_review = card['review_count'] + 1
            delta = 20 if knew_it else -10
            new_mastery = max(0, min(100, card['mastery_score'] + delta))
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            execute_query('''
                UPDATE flashcards SET review_count = ?, mastery_score = ?, last_reviewed = ? WHERE id = ?
            ''', (new_review, new_mastery, now, card_id), fetch_all=False)
            if knew_it:
                UserModel.add_xp(user_id, 5)

class WeakTopicModel:
    @staticmethod
    def update_topic_performance(user_id, topic, score, max_score):
        incorrect = max_score - score
        existing = execute_query("SELECT * FROM weak_topics WHERE user_id = ? AND topic = ?", (user_id, topic), fetch_all=False)
        if existing:
            tot_att = existing['total_attempted'] + max_score
            err_cnt = existing['error_count'] + incorrect
            acc = round(((tot_att - err_cnt) / tot_att) * 100.0, 1) if tot_att > 0 else 100.0
            prio = "High" if acc < 60 else ("Medium" if acc < 80 else "Low")
            execute_query('''
                UPDATE weak_topics SET total_attempted = ?, error_count = ?, accuracy_percentage = ?, priority = ?, last_evaluated = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (tot_att, err_cnt, acc, prio, existing['id']), fetch_all=False)
        else:
            tot_att = max(1, max_score)
            err_cnt = incorrect
            acc = round(((tot_att - err_cnt) / tot_att) * 100.0, 1)
            prio = "High" if acc < 60 else ("Medium" if acc < 80 else "Low")
            execute_query('''
                INSERT INTO weak_topics (user_id, topic, subject, error_count, total_attempted, accuracy_percentage, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, topic, 'Computer Science', err_cnt, tot_att, acc, prio), fetch_all=False)

    @staticmethod
    def get_weak_topics(user_id=1):
        return execute_query("SELECT * FROM weak_topics WHERE user_id = ? ORDER BY accuracy_percentage ASC", (user_id,))

class StudyPlanModel:
    @staticmethod
    def get_plans(user_id=1):
        return execute_query("SELECT * FROM study_plans WHERE user_id = ? ORDER BY plan_date ASC, id ASC", (user_id,))

    @staticmethod
    def toggle_task(task_id, current_status, user_id=1):
        new_status = 'completed' if current_status != 'completed' else 'pending'
        execute_query("UPDATE study_plans SET status = ? WHERE id = ?", (new_status, task_id), fetch_all=False)
        if new_status == 'completed':
            UserModel.add_xp(user_id, 20)
        return new_status

    @staticmethod
    def add_plan_item(user_id, title, plan_date, time_slot, topic, task_description):
        return execute_query('''
            INSERT INTO study_plans (user_id, title, plan_date, time_slot, topic, task_description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, title, plan_date, time_slot, topic, task_description), fetch_all=False)

class BadgeModel:
    @staticmethod
    def get_badges():
        return execute_query("SELECT * FROM badges ORDER BY unlocked_at DESC")

    @staticmethod
    def unlock_badge(code, name, desc, icon="🏆"):
        try:
            execute_query('''
                INSERT OR IGNORE INTO badges (badge_code, badge_name, badge_desc, icon)
                VALUES (?, ?, ?, ?)
            ''', (code, name, desc, icon), fetch_all=False)
        except Exception:
            pass

