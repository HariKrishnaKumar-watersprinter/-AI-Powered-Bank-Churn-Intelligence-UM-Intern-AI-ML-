import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os

# Use relative path (strongly recommended)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def signup_user(authenticator, config, config_path=CONFIG_PATH):
    st.subheader("📝 Create New Account")

    if not os.path.exists(config_path):
        st.error("Configuration file not found. Please restart the app.")
        return

   

    try:
        # ✅ Pre-authorization logic:
        # If the list has emails, only those emails can register.
        preauthorized_list = config.get('preauthorized', {}).get('emails')
        

        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            pre_authorized=preauthorized_list,
            location="main",
            clear_on_submit=True
        )

        if email_of_registered_user:
            # MUST update the local config object with the updated credentials from the authenticator
            
            # The 'config' object is automatically updated by the authenticator
            try:
                with open(config_path, 'w', encoding='utf-8') as file:
                    yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
                    st.success(f"✅ Account created successfully for **{name_of_registered_user}**!")
                    st.balloons()
                    st.info("You can now go to the **Login** tab and sign in.")
                    st.rerun()
            except Exception as save_err:
                st.error(f"Failed to save user: {save_err}")

    except Exception as e:
        error_str = str(e).lower()
        if "username already exists" in error_str:
            st.error("❌ Username already exists. Please choose a different username.")
        elif "email already exists" in error_str:
            st.error("❌ This email is already registered.")
        elif "not pre-authorized" in error_str:
            st.error("Registration is currently restricted.")
        else:
            st.error(f"Registration failed: {str(e)}")
