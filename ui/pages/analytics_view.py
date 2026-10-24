import streamlit as st
from ui.components import UIComponents
from features.analytics import AnalyticsFeature

def render_analytics_page():
    UIComponents.render_header(
        title="Performance Analytics",
        subtitle="Visualize your learning trajectory, topic mastery, and study metrics.",
        icon="📊"
    )

    metrics = AnalyticsFeature.get_dashboard_metrics()

    col1, col2, col3 = st.columns(3)
    with col1:
        UIComponents.render_metric_card("🎯", "Quiz Accuracy", f"{metrics['quiz_accuracy']}%")
    with col2:
        UIComponents.render_metric_card("⏱️", "Study Time", f"{metrics['study_hours']} hrs")
    with col3:
        UIComponents.render_metric_card("🃏", "Flashcards Reviewed", f"{metrics['card_count']} Cards")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.plotly_chart(AnalyticsFeature.create_accuracy_trend_chart(), use_container_width=True)
    with col_chart2:
        st.plotly_chart(AnalyticsFeature.create_topic_mastery_chart(), use_container_width=True)

    st.markdown("---")

    col_chart3, col_insights = st.columns([1, 1])
    with col_chart3:
        st.plotly_chart(AnalyticsFeature.create_study_time_chart(), use_container_width=True)

    with col_insights:
        st.markdown("### 🧠 AI Performance Insights")
        insights_md = AnalyticsFeature.generate_ai_insights()
        st.markdown(f'<div class="sm-card">{insights_md}</div>', unsafe_allow_html=True)
