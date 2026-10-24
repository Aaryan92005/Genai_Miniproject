import streamlit as st
from ui.components import UIComponents
from database.models import UserModel

def render_auth_page():
    UIComponents.render_header(
        title="Welcome to StudyMind 🧠",
        subtitle="Sign in to your private personal AI learning workspace or create a new student account.",
        icon="🔐"
    )

    st.markdown("""
    <div style="max-width: 480px; margin: 0 auto;">
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab_login:
        st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 16px;'>🔑 Student Login</h3>", unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="alex@university.edu")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("🚀 Sign In to StudyMind", use_container_width=True)

            if submit_login:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    user, msg = UserModel.authenticate(email, password)
                    if user:
                        st.session_state["authenticated_user"] = user
                        st.success(f"Welcome back, {user.get('name', 'Student')}!")
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("---")
        st.markdown("<h5 style='color: #f8fafc; font-weight: 700; margin-bottom: 10px;'>⚡ Quick Demo Access</h5>", unsafe_allow_html=True)
        if st.button("🔓 One-Click Demo Login (Instant Evaluation)", key="btn_demo_login", use_container_width=True):
            demo_user = UserModel.get_user(1)
            st.session_state["authenticated_user"] = demo_user
            st.rerun()

    with tab_register:
        st.markdown("<h3 style='color: #f8fafc; font-weight: 700; margin-bottom: 16px;'>📝 Create Student Account</h3>", unsafe_allow_html=True)
        with st.form("register_form"):
            reg_name = st.text_input("Full Name", placeholder="Alex Morgan")
            reg_email = st.text_input("Email Address", placeholder="alex@university.edu")
            reg_pwd = st.text_input("Create Password", type="password", placeholder="••••••••")
            reg_pwd_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            submit_reg = st.form_submit_button("✨ Register Account", use_container_width=True)

            if submit_reg:
                if not reg_name or not reg_email or not reg_pwd:
                    st.error("All fields are required.")
                elif reg_pwd != reg_pwd_confirm:
                    st.error("Passwords do not match!")
                elif len(reg_pwd) < 4:
                    st.error("Password must be at least 4 characters long.")
                else:
                    user, msg = UserModel.register(reg_name, reg_email, reg_pwd)
                    if user:
                        st.session_state["authenticated_user"] = user
                        st.success("Account created successfully! Welcome to StudyMind.")
                        st.rerun()
                    else:
                        st.error(msg)

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
