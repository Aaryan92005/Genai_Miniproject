class PromptTemplates:

    @staticmethod
    def get_tutor_system_prompt(mode="Explain", level="Intermediate"):
        level_instructions = {
            "Beginner": "Explain in simple, everyday language using analogies and basic terms. Avoid overly complex jargon.",
            "Intermediate": "Provide a balanced, clear, and comprehensive explanation suited for a undergraduate college student.",
            "Advanced": "Provide deep technical analysis, theoretical details, edge cases, formulas, and architecture specifics."
        }.get(level, "Provide a balanced, clear explanation.")

        mode_instructions = {
            "Explain": "Give a concise, direct, focused explanation of the specific concept asked by the student. Do NOT dump unrelated chapter subsections or topics.",
            "Teach": "Act as a master professor. Break down the specific topic step-by-step into logical sections, explaining 'why' before 'how'.",
            "Simple": "Explain like I am 10 years old. Use real-world analogies and ultra-simple metaphors.",
            "Exam": "Structure your response as a top-grade university exam answer for the specific question: 1. Definition 2. Core Principles 3. Pros/Cons 4. Real-world Example.",
            "Socratic": "DO NOT provide the direct answer immediately! Act as a Socratic tutor. Ask 1-2 insightful, probing questions that guide the student to discover the answer themselves."
        }.get(mode, "Give a structured, concise explanation.")

        return f"""You are StudyMind, an expert AI Personal Learning Companion and Academic Tutor.
Your goal is to help students master their study material effectively.

TARGET LEVEL: {level} ({level_instructions})
TUTORING MODE: {mode} ({mode_instructions})

IMPORTANT CONSTRAINTS:
1. Always base your knowledge primarily on the provided context passages from the student's study material.
2. If the answer cannot be found in the context passages, clearly state: "I couldn't find enough information in your uploaded study material." and then provide a general explanation if applicable, clearly flagging it as general knowledge.
3. Use clean markdown, bold terms, bullet points, and code/math blocks where helpful.
4. Keep the tone encouraging, professional, and clear.
"""

    @staticmethod
    def get_quiz_generation_prompt(context, topic, num_questions=5, difficulty="Medium", question_type="MCQ"):
        return f"""Generate a high-yield academic quiz of {num_questions} questions on the topic "{topic}" at {difficulty} difficulty using STRICTLY the provided study material below.

QUESTION TYPE: {question_type}

STUDY MATERIAL CONTEXT:
{context}

CRITICAL ACCURACY CONSTRAINTS:
1. Every question MUST be directly answerable from the provided study material context. Do NOT invent outside facts.
2. For MCQs and True-False questions, the "correct_answer" string MUST match EXACTLY one of the strings inside the "options" array.
3. Include a verbatim "source_snippet" from the context material that proves the answer.
4. "explanation" must clearly justify why the correct answer is right based on the source text.

Return ONLY valid, parseable JSON matching this exact structure:
[
  {{
    "id": 1,
    "question": "Question text here?",
    "type": "{question_type}",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option B",
    "explanation": "Detailed explanation of why Option B is correct based on the source text.",
    "source_snippet": "Verbatim quote from document proving the answer."
  }}
]

Output strict JSON only. No markdown intro/outro.
"""

    @staticmethod
    def get_flashcard_prompt(context, topic, num_cards=5):
        return f"""Create {num_cards} high-yield study flashcards for the topic "{topic}" based on the context below.

CONTEXT:
{context}

Return ONLY valid JSON matching this exact structure:
[
  {{
    "id": 1,
    "topic": "{topic}",
    "question": "Clear concept or question",
    "answer": "Concise, memorable answer with key terms",
    "difficulty": "Medium"
  }}
]

Output strict JSON only. No markdown intro/outro.
"""

    @staticmethod
    def get_summary_prompt(context, document_name, depth="Medium"):
        depth_instructions = {
            "Short": "Keep the summary ultra-concise (under 250 words). Focus only on executive high-yield bullet points.",
            "Medium": "Provide a balanced academic summary (500-750 words) with key concepts, formulas, and exam questions.",
            "Detailed": "Provide an exhaustive, highly detailed study guide (1000+ words). Expand every subsection thoroughly with full explanations, formulas, 5 university exam questions with model answers, and a detailed section-by-section breakdown."
        }.get(depth, "Provide a balanced academic summary.")

        return f"""Analyze the provided study document material from "{document_name}" and generate a high-yield study summary.

SUMMARY DEPTH: {depth} ({depth_instructions})

CONTEXT MATERIAL:
{context}

Please structure your response cleanly using Markdown:

### 📌 Executive Summary
(Overview of main subject)

### 💡 Key Concepts & Definitions
(Bulleted list of concepts with clear explanations)

### 📐 Important Formulas & Rules
(Mathematical equations, algorithms, or formal rules)

### 🎯 Likely Exam Questions
(3-5 university exam style questions with answer guidance)

### ⚡ One-Minute Exam Revision
(Bullet points for last-minute review)

### 📖 Detailed Notes & Section Breakdown
(Exhaustive conceptual breakdown)
"""

    @staticmethod
    def get_study_plan_prompt(subjects, exam_date, daily_hours, weak_topics):
        return f"""Act as an AI Academic Study Counselor. Generate a structured, realistic daily study schedule.

INPUT DETAILS:
- Subjects/Topics: {subjects}
- Target Exam Date: {exam_date}
- Daily Study Hours: {daily_hours} hrs/day
- Student Weak Topics: {weak_topics}

Return ONLY valid JSON representing daily tasks for the upcoming study period matching this structure:
[
  {{
    "title": "DBMS Normalization Practice",
    "plan_date": "2026-09-03",
    "time_slot": "09:00 - 10:30 AM",
    "topic": "Database Management Systems",
    "task_description": "Review 2NF/3NF dependencies and solve 5 practice problems."
  }}
]
Output strict JSON array.
"""

    @staticmethod
    def get_weakness_fix_prompt(topic, context):
        return f"""You are StudyMind AI Revision Master. The student is currently struggling with "{topic}".
Analyze the provided study context and build a targeted "Fix My Weakness" mini learning package.

CONTEXT:
{context}

Structure your response as follows:
### 1. 🔍 Conceptual Clarity (Where students get confused)
(Identify the exact point of confusion and explain it simply)

### 2. 💡 Concrete Example & Analogy
(Provide a step-by-step worked example)

### 3. 🎯 3-Step Practice Drill
(3 quick check questions with instant answers below)

### 4. 🔑 Golden Rule to Remember
(1 key sentence memory trick)
"""
