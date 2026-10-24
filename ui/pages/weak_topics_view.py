import streamlit as st
from ui.components import UIComponents
from features.weak_topics import WeakTopicFeature

def render_weak_topics_page():
    UIComponents.render_header(
        title="Weak Topic Detection & AI Revision",
        subtitle="Identify conceptual gaps from quiz attempts and launch targeted 'Fix My Weakness' revision loops.",
        icon="🧠"
    )

    weak_list = WeakTopicFeature.get_weak_topics()

    if not weak_list:
        st.success("🎉 No weak topics detected! Your overall quiz accuracy is high across all subjects.")
        return

    st.markdown("### 🔴 Identified Weak Concept Areas")

    for item in weak_list:
        acc = item["accuracy_percentage"]
        prio = item["priority"]
        color = "#ef4444" if prio == "High" else ("#f59e0b" if prio == "Medium" else "#10b981")
        icon = "🔴" if prio == "High" else ("🟡" if prio == "Medium" else "🟢")

        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{icon} {item['topic']}** (`{item.get('subject', 'General')}`)")
                st.progress(max(0.05, acc / 100.0))
                st.caption(f"Accuracy: {acc}% | Total Attempts: {item['total_attempted']} | Mistakes: {item['error_count']}")

            with col2:
                if st.button("✨ Fix My Weakness", key=f"btn_fix_{item['id']}"):
                    st.session_state["active_weak_topic"] = item["topic"]
                    st.rerun()

            st.divider()

    # Active "Fix My Weakness" Revision Package
    active_weak = st.session_state.get("active_weak_topic")
    if active_weak:
        st.markdown("---")
        st.markdown(f"## 🛠️ AI Remedial Package: `{active_weak}`")
        
        with st.spinner(f"Generating targeted concept breakdown & practice drill for {active_weak}..."):
            fix_md = WeakTopicFeature.generate_fix_my_weakness_package(active_weak)
            st.markdown(f'<div class="sm-card">{fix_md}</div>', unsafe_allow_html=True)
