import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """
    Central configuration management for DataEngOS.
    Persists settings to ~/.dataengos/config.toml or local .env
    For MVP, we use Streamlit secrets or OS env vars primarily.
    """
    
    @staticmethod
    def get_api_key():
        # Priority: Session State > OS Env (usually .env)
        if "api_key" in st.session_state:
            return st.session_state["api_key"]
        return os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

    @staticmethod
    def get_provider():
        if "llm_provider" in st.session_state:
            return st.session_state["llm_provider"]
        return os.getenv("LLM_PROVIDER", "gemini/gemini-1.5-flash") # Default to Gemini 1.5 Flash

    @staticmethod
    def save_config(api_key: str, provider: str):
        """
        Saves configuration to session state and optionally to local .env for persistence in dev.
        """
        st.session_state["api_key"] = api_key
        st.session_state["llm_provider"] = provider
        
        # Simple persistence for dev convenience
        env_path = Path(".env")
        with open(env_path, "w") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
            f.write(f"LLM_PROVIDER={provider}\n")

config = Config()
