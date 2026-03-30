import streamlit as st
import yaml
import secrets
import string
import streamlit_authenticator as stauth
from Authentication.config import config_user
from Authentication.signup import signup_user
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def user_auth():
    authenticator, config = config_user()
    
    # 1. Handle Logged-In State (Hide Tabs)
    if st.session_state.get('authentication_status'):
        # Password Management for Active Sessions
        authenticator.logout("🚪 Logout", location="sidebar", key="logout_widget")
        if st.sidebar.checkbox("Change my password"):
            username = st.session_state.get('username')
            try:
                if authenticator.reset_password(username, location="sidebar", key="reset_pw"):
                    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.success("✅ Password updated successfully!")
            except Exception as e:
                st.error(f"Reset error: {e}")
        st.success(f"✅ Welcome, **{st.session_state.get('name')}**!")
        return True
    st.write("---")
    # 2. Handle Logged-Out State (Show Tabs)
    st.title("🏦 Bank Churn Prediction System")
    st.markdown("### Secure Login Required")
    tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Sign Up", "🔐 Forgot Password"])

    with tab1:
        authenticator.login(location="main", key="login_widget")
        
        # Check status after widget interaction
        auth_status = st.session_state.get('authentication_status')
         # Immediately switch to Logged-In UI
        
        if auth_status is False:
            st.error("❌ Username or password is incorrect")
        elif auth_status is None:
            st.warning("👋 Please enter your username and password")

    with tab2:
        signup_user(authenticator, config)

    with tab3:
        st.subheader("🔐 Forgot Password")
        email_to_reset = st.text_input("Enter your registered Email ID", key="forgot_email_input")
        
        if st.button("Generate New Password", key="forgot_password_btn"):
            if email_to_reset:
                found_username = None
                # Iterate through credentials to find the username matching this email
                for username, user_info in config['credentials']['usernames'].items():
                    if user_info.get('email') == email_to_reset:
                        found_username = username
                        break
                
                if found_username:
                    # 1. Generate a random temporary password
                    new_pw = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
                    
                    # 2. Hash the new password using the library's static method (v0.3.0+)
                    hashed_pw = stauth.Hasher.hash(new_pw)
                    
                    # 3. Update the password in the config dictionary
                    config['credentials']['usernames'][found_username]['password'] = hashed_pw
                    
                    # 4. Save the updated configuration back to the YAML file
                    try:
                        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        
                        st.success(f"✅ New password generated for user: **{found_username}**")
                        st.info("Please use the password below to log in.")
                        st.code(new_pw, language=None)
                        st.warning("⚠️ Important: Log in and change this password immediately for security.")
                    except Exception as save_err:
                        st.error(f"Critical error: Could not update the database. {save_err}")
                else:
                    st.error("❌ No account found with that email address. Please check and try again.")
            else:
                st.warning("Please enter your registered email address.")
            
    return st.session_state.get('authentication_status', False)


if __name__ == "__main__":
    user_auth()