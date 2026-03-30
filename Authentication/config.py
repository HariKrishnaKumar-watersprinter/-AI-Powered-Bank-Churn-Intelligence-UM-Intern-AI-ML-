import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx
import yaml
from yaml.loader import SafeLoader
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")




def load_config():
    """Safely load or create config.yaml"""
    if not os.path.exists(CONFIG_PATH):
        # Create default config if file doesn't exist
        default_config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@example.com',
                        'name': 'Admin User',
                        'password': '$2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # ← MUST replace with real hash
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'bank_churn_secret_key_2026',
                'name': 'bankchurn_auth_cookie'
            },
            'preauthorized': {
                'emails': []
            }
        }
        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
            yaml.dump(default_config, file, default_flow_style=False, allow_unicode=True)
        
        st.success("✅ Default config.yaml created. Please replace the dummy password with a real hashed one.")
        return default_config

    # File exists → load it safely
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=SafeLoader)
        
        # Handle case where yaml.load returns None (empty or invalid file)
        if config is None:
            config = {}
        
        # Ensure required keys exist
        if 'credentials' not in config:
            config['credentials'] = {'usernames': {}}
        if 'cookie' not in config:
            config['cookie'] = {
                'expiry_days': 30,
                'key': 'bank_churn_secret_key_2026',
                'name': 'bankchurn_auth_cookie'
            }
        if 'preauthorized' not in config:
            config['preauthorized'] = {'emails': []}
            
        return config

    except Exception as e:
        st.error(f"Error reading config.yaml: {e}")
        st.info("Deleting corrupted config.yaml and creating a new one...")
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
        return load_config()  # Recursive call to recreate


def config_user():
    config = load_config()

    # Correctly extract the list of emails or set to None for open registration
    preauthorized_emails = config.get('preauthorized', {}).get('emails')
    if not preauthorized_emails:
        preauthorized_emails = None

    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        cookie_key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days'],
        preauthorized=preauthorized_emails
    )

    return authenticator, config