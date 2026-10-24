import sqlite3
import json
import logging
from datetime import datetime
from config.settings import DB_PATH

logger = logging.getLogger(__name__)

def get_connection():
    """Returns a SQLite connection with dict row factory."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database schema if tables do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT DEFAULT 'Student',
            email TEXT UNIQUE,
            password_hash TEXT,
            target_exam_date TEXT,
            daily_hours REAL DEFAULT 2.0,
            level INTEGER DEFAULT 1,
            xp_points INTEGER DEFAULT 0,
            streak_count INTEGER DEFAULT 1,
            last_active_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add password_hash column if missing in existing DB
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    except Exception:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except Exception:
        pass

    # 2. Documents Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER DEFAULT 0,
            page_count INTEGER DEFAULT 1,
            chunk_count INTEGER DEFAULT 0,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'processed',
            topics_json TEXT DEFAULT '[]',
            summary_json TEXT DEFAULT '{}'
        )
    ''')

    try:
        cursor.execute("ALTER TABLE documents ADD COLUMN user_id INTEGER DEFAULT 1")
    except Exception:
        pass

    # 3. Document Chunks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id INTEGER NOT NULL,
            user_id INTEGER DEFAULT 1,
            chunk_index INTEGER NOT NULL,
            page_number INTEGER DEFAULT 1,
            content TEXT NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents (id) ON DELETE CASCADE
        )
    ''')

    try:
        cursor.execute("ALTER TABLE document_chunks ADD COLUMN user_id INTEGER DEFAULT 1")
    except Exception:
        pass

    # 4. Quiz Attempts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            topic TEXT NOT NULL,
            difficulty TEXT DEFAULT 'Medium',
            question_type TEXT DEFAULT 'MCQ',
            score INTEGER DEFAULT 0,
            max_score INTEGER DEFAULT 0,
            percentage REAL DEFAULT 0.0,
            time_taken_sec INTEGER DEFAULT 0,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details_json TEXT DEFAULT '[]'
        )
    ''')

    try:
        cursor.execute("ALTER TABLE quiz_attempts ADD COLUMN user_id INTEGER DEFAULT 1")
    except Exception:
        pass

    # 5. Flashcards Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            doc_id INTEGER,
            topic TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            difficulty TEXT DEFAULT 'Medium',
            review_count INTEGER DEFAULT 0,
            mastery_score INTEGER DEFAULT 0,
            last_reviewed TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    try:
        cursor.execute("ALTER TABLE flashcards ADD COLUMN user_id INTEGER DEFAULT 1")
    except Exception:
        pass

    # 6. Study Sessions Log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            topic TEXT NOT NULL,
            duration_minutes INTEGER DEFAULT 30,
            session_type TEXT DEFAULT 'Quiz',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')

    try:
        cursor.execute("ALTER TABLE study_sessions ADD COLUMN user_id INTEGER DEFAULT 1")
    except Exception:
        pass

    # 7. Study Plans Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            plan_date TEXT NOT NULL,
            time_slot TEXT,
            topic TEXT NOT NULL,
            task_description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    try:
        cursor.execute("ALTER TABLE study_plans ADD COLUMN user_id INTEGER DEFAULT 1")
    except Exception:
        pass

    # 8. Weak Topics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weak_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            topic TEXT NOT NULL,
            subject TEXT DEFAULT 'General',
            error_count INTEGER DEFAULT 1,
            total_attempted INTEGER DEFAULT 1,
            accuracy_percentage REAL DEFAULT 0.0,
            priority TEXT DEFAULT 'High',
            last_evaluated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    try:
        cursor.execute("ALTER TABLE weak_topics ADD COLUMN user_id INTEGER DEFAULT 1")
    except Exception:
        pass

    # 9. Badges / Gamification
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            badge_code TEXT UNIQUE NOT NULL,
            badge_name TEXT NOT NULL,
            badge_desc TEXT NOT NULL,
            icon TEXT DEFAULT '🏆',
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Default User check
    cursor.execute('SELECT COUNT(*) as count FROM users')
    if cursor.fetchone()['count'] == 0:
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO users (name, target_exam_date, daily_hours, level, xp_points, streak_count, last_active_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('Student', '2026-10-15', 2.5, 1, 150, 3, today))

    conn.commit()
    conn.close()
    logger.info("Database schema initialized successfully.")

def execute_query(query, params=(), fetch_all=True):
    """Executes a SQL query and returns results as dicts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    if query.strip().upper().startswith("SELECT"):
        rows = cursor.fetchall() if fetch_all else cursor.fetchone()
        result = [dict(r) for r in rows] if fetch_all and rows else (dict(rows) if rows else ([] if fetch_all else None))
    else:
        conn.commit()
        result = cursor.lastrowid
    conn.close()
    return result

# Initialize on import
init_db()
