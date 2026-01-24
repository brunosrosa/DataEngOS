import json
import streamlit as st
from litellm import completion
from dataeng_os.config import config

class Architect:
    """
    The Intelligence Layer of DataEngOS.
    Uses LiteLLM to interface with Gemini, OpenAI, etc.
    """
    
    def __init__(self):
        pass

    def _get_llm_response(self, messages, json_mode=False, model_override=None):
        api_key = config.get_api_key()
        # specific tasks can force a model (e.g. Flash for speed/intent)
        model = model_override or config.get_provider()
        
        if not api_key:
            return None # Should handle gracefully in UI
            
        try:
            response = completion(
                model=model,
                messages=messages,
                api_key=api_key,
                response_format={"type": "json_object"} if json_mode else None
            )
            content = response.choices[0].message.content
            return content
        except Exception as e:
            st.error(f"LLM Error ({model}): {e}")
            return None

    def analyze_intent(self, user_input: str) -> dict:
        """
        Detects if the user wants to create a contract or just chat.
        Uses a Fast/Cheap model (Gemini Flash) to avoid using Pro quota.
        """
        system_prompt = """
        You are the DataEngOS Architect. Analyze the user's input.
        If they want to create a new data contract/table/dataset, return JSON: {"action": "create_contract", "topic": "summary of topic"}.
        If they just want to chat or ask questions, return JSON: {"action": "chat", "topic": null}.
        Example Input: "I want to ingest sales data" -> {"action": "create_contract", "topic": "sales data ingestion"}
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        # Force Flash for Intent Analysis (Low Reasoning, High RPM)
        # We try to use the configured provider's "fast" equivalent if possible, 
        # but for this specific patch we prioritize the user's suggestion: gemini-3-flash-preview
        fast_model = "gemini/gemini-3-flash-preview"
        
        response = self._get_llm_response(messages, json_mode=True, model_override=fast_model)
        if response:
            try:
                return json.loads(response)
            except:
                return {"action": "chat", "topic": None} # Fallback
        
        # Mock Fallback if no key or error
        return self._mock_analyze_intent(user_input)

    def chat(self, user_input: str) -> str:
        """
        Conversational response.
        """
        system_prompt = "You are a helpful Data Engineer Architect. Helping the user build valid data contracts."
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
        
        response = self._get_llm_response(messages)
        if response:
            return response
            
        return "I need an API Key to think! Please configure it in Settings."

    def generate_draft(self, scenario_description: str) -> dict:
        """
        Generates a initial contract draft from description.
        """
        system_prompt = """
        Generate a Data Contract JSON structure based on the user description.
        Output MUST be valid JSON with this structure:
        {
            "dataset": { "domain": "string", "logical_name": "string", "physical_name": "string", "description": "string", "owners": [{"team": "string", "email": "string"}] },
            "schema": [ {"name": "col_name", "type": "string|int|timestamp|decimal", "desc": "description", "pk": boolean} ],
            "slas": { "frequency": "daily|hourly|streaming", "freshness": "24h" }
        }
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a contract for: {scenario_description}"}
        ]
        
        response = self._get_llm_response(messages, json_mode=True)
        if response:
            try:
                return json.loads(response)
            except:
                st.error("Failed to parse LLM JSON")
                return {}
        
        return self._mock_generate_draft(scenario_description)

    # --- MOCK FALLBACKS (For when Key is missing) ---
    def _mock_analyze_intent(self, user_input):
        user_input = user_input.lower()
        if any(w in user_input for w in ["criar", "nova", "novo", "create", "new", "tabela", "contrato"]):
            return {"action": "create_contract", "topic": user_input}
        return {"action": "chat", "topic": None}

    def _mock_generate_draft(self, topic):
        return {
            "dataset": {
                "domain": "mock_domain",
                "logical_name": "mock_table",
                "description": f"Generated (Mock) for {topic}",
                "owners": [{"team": "Data Team", "email": "bot@dataengos.io"}]
            },
            "schema": [
                {"name": "id", "type": "string", "desc": "Mock ID", "pk": True}
            ],
            "slas": {"frequency": "daily", "freshness": "24h"}
        }

# Global Singleton
architect = Architect()
