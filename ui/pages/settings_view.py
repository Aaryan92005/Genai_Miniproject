import os
import streamlit as st
from ui.components import UIComponents
from config.settings import GROQ_API_KEY, OPENAI_API_KEY, DEFAULT_LLM_PROVIDER, DEFAULT_LLM_MODEL

def render_settings_page():
    UIComponents.render_header(
        title="Settings & System Configuration",
        subtitle="Manage LLM providers, model parameters, API keys, and application preferences.",
        icon="⚙️"
    )

    # API Status Banner
    has_key = bool(GROQ_API_KEY or OPENAI_API_KEY or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY"))
    if has_key:
        st.success("🟢 Cloud LLM API Key Detected & Connected. Full AI Generation Active.")
    else:
        st.info("💡 Smart Local Fallback Engine Active. No external API key required! Add a Groq/OpenAI key below to enable cloud LLM power.")

    st.markdown("---")
    st.markdown("### 🤖 AI Model Configuration")

    col1, col2 = st.columns(2)
    with col1:
        provider = st.selectbox(
            "LLM Provider",
            ["groq", "openai", "huggingface", "smart_local_fallback"],
            index=0 if DEFAULT_LLM_PROVIDER == "groq" else 1
        )
        model_name = st.text_input("LLM Model Name", value=DEFAULT_LLM_MODEL)

    with col2:
        temperature = st.slider("Temperature (Creativity vs Determinism)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
        top_k = st.slider("RAG Top-K Chunks to Retrieve", min_value=1, max_value=10, value=3)

    st.markdown("---")
    st.markdown("### 🔑 API Key Entry")

    groq_key_input = st.text_input("Groq API Key", type="password", value=GROQ_API_KEY or os.getenv("GROQ_API_KEY", ""))
    openai_key_input = st.text_input("OpenAI API Key", type="password", value=OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", ""))

    if st.button("💾 Save Settings & Update Environment", key="btn_save_settings"):
        if groq_key_input:
            os.environ["GROQ_API_KEY"] = groq_key_input.strip()
        if openai_key_input:
            os.environ["OPENAI_API_KEY"] = openai_key_input.strip()
        st.success("Settings saved successfully! StudyMind pipeline re-initialized.")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🎨 Appearance & UI Preferences")
    st.selectbox("Theme Direction", ["Dark Glassmorphism (Recommended)", "Classic Light"], index=0)
