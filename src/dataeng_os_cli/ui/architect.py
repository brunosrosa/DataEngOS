import json
import streamlit as st
from litellm import completion
from pathlib import Path
import yaml
from dataeng_os.config import config

class Architect:
    """
    The Intelligence Layer of DataEngOS.
    Uses LiteLLM to interface with Gemini, OpenAI, etc.
    Now Context-Aware: Scans local contracts to act as a "Chief Architect".
    """
    
    def __init__(self):
        self.catalog_index = {}
        # Lazy load or load on init? For now, load on first chat or init if cheap.
        # We'll do a lightweight scan now.
        self._index_catalog()

    def _index_catalog(self):
        """
        Scans projects/**/contracts/**/*.yaml to build a lightweight index.
        Stores keywords to help the LLM understand what exists.
        """
        base_path = Path("projects")
        if not base_path.exists():
            return

        # Reset
        self.catalog_index = {}

        # Glob all YAMLs in contracts folders
        yaml_files = list(base_path.glob("**/contracts/**/*.yaml"))
        
        for yf in yaml_files:
            try:
                with open(yf, 'r') as f:
                    data = yaml.safe_load(f)
                
                dataset = data.get("dataset", {})
                name = dataset.get("logical_name") or yf.stem
                domain = dataset.get("domain", "unknown")
                desc = dataset.get("description", "No description")
                
                # Store simplified metadata
                self.catalog_index[name] = {
                    "domain": domain,
                    "description": desc,
                    "path": str(yf)
                }
            except Exception:
                # Silently fail for now or log
                continue

    def _get_catalog_context(self) -> str:
        """
        Generates a concise summary of the catalog for the System Prompt.
        """
        if not self.catalog_index:
            return "Catalog is empty. No existing data contracts found."
            
        summary_lines = ["Existing Data Contracts in Catalog:"]
        for name, meta in self.catalog_index.items():
            summary_lines.append(f"- {name} (Domain: {meta['domain']}): {meta['description']}")
        
        return "\n".join(summary_lines)

    def _get_llm_response(self, messages, json_mode=False, model_override=None):
        api_key = config.get_api_key()
        # use config for model resolution
        model = model_override or config.get_model_name("standard")
        
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
        Uses a Fast/Cheap model to avoid using Pro quota.
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
        
        # Use "fast" tier for high RPM/low latency
        fast_model = config.get_model_name("fast")
        
        response = self._get_llm_response(messages, json_mode=True, model_override=fast_model)
        if response:
            try:
                return json.loads(response)
            except Exception:
                return {"action": "chat", "topic": None} # Fallback
        
        # Mock Fallback if no key or error
        return self._mock_analyze_intent(user_input)

    def chat(self, user_input: str) -> str:
        """
        Conversational response with Catalog Context.
        Persona: Chief Architect.
        """
        # Re-index on chat to capture recent changes? (Optional, maybe optimization later)
        # self._index_catalog() 
        
        catalog_context = self._get_catalog_context()
        
        system_prompt = f"""
        You are the **Chief Architect** of this Data Platform (DataEngOS).
        You are opinionated, precise, and helpful. You prefer standard Data Product patterns.
        
        **Context - Existing Catalog:**
        {catalog_context}
        
        **Guidelines:**
        1. If the user asks about existing data, refer to the Catalog Context above.
        2. If the user proposes a redundant dataset, warn them.
        3. Be concise. Use technical language appropriate for data engineers.
        """
        
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
        
        # Use "reasoning" tier if available for better chat, or standard
        model = config.get_model_name("reasoning")
        
        response = self._get_llm_response(messages, model_override=model)
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
        
        # Draft generation benefits from reasoning models too
        model = config.get_model_name("reasoning")

        response = self._get_llm_response(messages, json_mode=True, model_override=model)
        if response:
            try:
                return json.loads(response)
            except Exception:
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
