import logging
from database.models import WeakTopicModel
from core.vector_store import global_vector_store
from core.prompts import PromptTemplates
from core.llm import LLMEngine

logger = logging.getLogger(__name__)

class WeakTopicFeature:
    @classmethod
    def get_weak_topics(cls):
        """Returns list of weak topics sorted by lowest accuracy."""
        topics = WeakTopicModel.get_weak_topics()
        if not topics:
            # Starter seed topics if DB is new
            WeakTopicModel.update_topic_performance("DBMS Normalization (2NF/3NF)", 2, 5) # 40%
            WeakTopicModel.update_topic_performance("OS Deadlock Detection", 4, 6) # 66.7%
            WeakTopicModel.update_topic_performance("Computer Networks Subnetting", 8, 9) # 88.9%
            topics = WeakTopicModel.get_weak_topics()
        return topics

    @classmethod
    def generate_fix_my_weakness_package(cls, topic):
        """Generates targeted AI revision package for a specific weak topic."""
        search_results = global_vector_store.search(topic, top_k=4)
        context = "\n\n".join([s["content"] for s in search_results]) if search_results else f"Study material for {topic}."

        prompt = PromptTemplates.get_weakness_fix_prompt(topic, context)
        system_prompt = "You are StudyMind AI Revision Master. Create deep, clear remedial revision guides."

        revision_md = LLMEngine.generate(prompt, system_prompt=system_prompt)
        return revision_md
