import streamlit as st

class UIComponents:
    @staticmethod
    def render_header(title, subtitle=None, icon="🧠", badge="STUDYMIND OS"):
        st.markdown(f"""
        <div style="margin-bottom: 28px;">
            <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.25); padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; color: #818cf8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;">
                <span>✨</span> <span>{badge}</span>
            </div>
            <h1 style="font-size: 2.3rem; font-weight: 800; color: #f8fafc; margin-bottom: 6px; display: flex; align-items: center; gap: 10px;">
                <span>{icon}</span>
                <span style="background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</span>
            </h1>
            {f'<p style="color: #94a3b8; font-size: 1.05rem; margin-top: 0; font-weight: 400; line-height: 1.5;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_metric_card(icon, label, value, subtext=None):
        st.markdown(f"""
        <div class="sm-card" style="padding: 22px; text-align: left;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <div class="sm-metric-label">{label}</div>
                <div class="sm-icon-box" style="margin-bottom: 0;">{icon}</div>
            </div>
            <div class="sm-metric-val" style="margin-bottom: 4px;">{value}</div>
            {f'<div style="font-size: 0.78rem; color: #64748b; font-weight: 500;">{subtext}</div>' if subtext else ''}
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_ai_insight_card(title, content, button_key="explain_insight"):
        st.markdown(f"""
        <div class="sm-card-gradient">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(168, 85, 247, 0.25); border: 1px solid rgba(168, 85, 247, 0.4); display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">
                    💡
                </div>
                <h3 style="margin: 0; font-size: 1.18rem; color: #ffffff; font-weight: 700;">{title}</h3>
            </div>
            <p style="color: #cbd5e1; font-size: 0.96rem; line-height: 1.6; margin-bottom: 0;">
                {content}
            </p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_source_chips(sources):
        if not sources:
            return
        st.markdown("#### 📄 Sources & Grounded Passages")
        chips_html = ""
        for s in sources:
            chips_html += f"""
            <div class="sm-chip">
                <span>📄</span> <span>{s['filename']}</span> <span style="opacity: 0.6;">(Pg {s['page_number']})</span> <span style="background: rgba(99, 102, 241, 0.3); padding: 2px 6px; border-radius: 6px; color: #c084fc; font-weight: 700;">{int(s['score']*100)}% Match</span>
            </div>
            """
        st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)

    @staticmethod
    def render_transparency_accordion(transparency_data):
        if not transparency_data:
            return
        with st.expander("🔍 How StudyMind Answered (RAG Transparency & Grounding)"):
            st.write(f"**Query Processed:** `{transparency_data.get('query')}`")
            st.write(f"**Tutoring Mode:** `{transparency_data.get('tutor_mode')}` | **Explanation Level:** `{transparency_data.get('level')}`")
            st.write(f"**Retrieved Chunks:** `{transparency_data.get('retrieved_count')}` passages from vector database")
            st.write(f"**Grounding Confidence Score:** `{transparency_data.get('grounding_confidence')*100}%`")
            st.write("**Top Similarity Scores:**", transparency_data.get("similarity_scores"))
            st.write("**System Prompt Context:**")
            st.code(transparency_data.get("system_prompt_sample"), language="markdown")
