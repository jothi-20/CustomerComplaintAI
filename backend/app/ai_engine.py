# app/ai_engine.py

import httpx
from datetime import datetime

# Internal GenAI endpoint client
client = httpx.Client(verify=False)

BASE_URL = "https://genailab.tcs.in"
MODEL_NAME = "azure_ai/genailab-maas-Phi-4-reasoning"
API_KEY = "sk--8jBe3cpv60PpIgw8brdhQ"  # Replace with your actual key

# Prompt template
PROMPT_TEMPLATE = """
You are a professional banking customer support assistant. 
Transform the following raw customer interaction into a structured case note. 

Requirements:
1. Interaction Summary
2. Action Taken
3. Next Steps
4. Suggested Tags (2-5, comma-separated)

Raw Note:
{raw_note}
"""

def generate_case_note(raw_note: str):
    prompt = PROMPT_TEMPLATE.format(raw_note=raw_note)

    try:
        response = client.post(
            f"{BASE_URL}/v1/predict",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": MODEL_NAME, "input": prompt},
            timeout=60
        ).json()

        # Get the text output (depends on your internal API structure)
        # Assuming response contains {'output_text': '...'}
        text_output = response.get("output_text", raw_note)

    except Exception:
        text_output = raw_note

    result = {"interaction_summary": "", "action_taken": "", "next_steps": "", "tags": []}

    for line in text_output.split("\n"):
        line_lower = line.lower()
        if line_lower.startswith("interaction summary:"):
            result["interaction_summary"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("action taken:"):
            result["action_taken"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("next steps:"):
            result["next_steps"] = line.split(":", 1)[1].strip()
        elif line_lower.startswith("suggested tags:"):
            tags_str = line.split(":", 1)[1].strip()
            result["tags"] = [t.strip() for t in tags_str.split(",") if t.strip()]

    # fallback defaults
    if not result["interaction_summary"]:
        result["interaction_summary"] = raw_note[:100] + "..."
    if not result["action_taken"]:
        result["action_taken"] = "Investigated issue."
    if not result["next_steps"]:
        result["next_steps"] = "Follow up within SLA period."

    return result