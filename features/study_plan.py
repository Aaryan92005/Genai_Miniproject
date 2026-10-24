import json
import re
import logging
from datetime import datetime, timedelta
from core.prompts import PromptTemplates
from core.llm import LLMEngine
from database.models import StudyPlanModel, WeakTopicModel

logger = logging.getLogger(__name__)

class StudyPlanFeature:
    @classmethod
    def generate_personalized_plan(cls, subjects="Operating Systems, DBMS, Computer Networks", exam_date="2026-10-15", daily_hours=2.5):
        """Generates AI personalized study schedule adapted to student's weak areas."""
        weak_topics = WeakTopicModel.get_weak_topics()
        weak_str = ", ".join([f"{w['topic']} ({w['accuracy_percentage']}%)" for w in weak_topics[:3]]) if weak_topics else "None recorded yet."

        prompt = PromptTemplates.get_study_plan_prompt(subjects, exam_date, daily_hours, weak_str)
        system_prompt = "You are StudyMind AI Study Planner. Output strictly valid JSON arrays of study schedule items."

        raw = LLMEngine.generate(prompt, system_prompt=system_prompt, json_mode=True)

        try:
            clean_raw = re.sub(r'^```json\s*', '', raw, flags=re.MULTILINE)
            clean_raw = re.sub(r'^```\s*', '', clean_raw, flags=re.MULTILINE).strip()
            plan_items = json.loads(clean_raw)
            if not isinstance(plan_items, list):
                plan_items = [plan_items]
        except Exception:
            plan_items = json.loads(LLMEngine._generate_fallback_json("study plan"))

        # Save generated tasks into DB
        for item in plan_items:
            StudyPlanModel.add_plan_item(
                title=item.get("title", "Study Session"),
                plan_date=item.get("plan_date", datetime.now().strftime("%Y-%m-%d")),
                time_slot=item.get("time_slot", "09:00 AM"),
                topic=item.get("topic", "General"),
                task_description=item.get("task_description", "Review core concepts")
            )

        return StudyPlanModel.get_plans()

    @classmethod
    def get_plans(cls):
        plans = StudyPlanModel.get_plans()
        if not plans:
            # Seed default starter plan
            cls.generate_personalized_plan()
            plans = StudyPlanModel.get_plans()
        return plans

    @classmethod
    def toggle_task(cls, task_id, current_status):
        return StudyPlanModel.toggle_task(task_id, current_status)
