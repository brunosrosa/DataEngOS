import json
import os
import streamlit as st
from pathlib import Path

# Simple Singleton to load locales
class I18n:
    _instance = None
    _locales = {}
    _current_lang = "pt_br"  # Default to PT-BR for this MVP

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18n, cls).__new__(cls)
            cls._instance._load_locales()
        return cls._instance

    def _load_locales(self):
        # Load pt_br.json
        base_path = Path(__file__).parent / "locales"
        try:
            with open(base_path / "pt_br.json", "r", encoding="utf-8") as f:
                self._locales["pt_br"] = json.load(f)
            
            with open(base_path / "en_us.json", "r", encoding="utf-8") as f:
                self._locales["en_us"] = json.load(f) 
        except Exception as e:
            # Fallback if file not found
            print(f"Error loading locales: {e}")
            self._locales["pt_br"] = {}

    def t(self, key: str) -> str:
        # Get from Session State if toggled, otherwise default
        lang = st.session_state.get("lang", self._current_lang)
        
        # Simple lookup
        return self._locales.get(lang, {}).get(key, key)

    def set_lang(self, lang: str):
        self._current_lang = lang
        st.session_state["lang"] = lang

# Helper function for easy import
def t(key: str) -> str:
    return I18n().t(key)
