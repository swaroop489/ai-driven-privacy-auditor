import os
import json
import traceback
from typing import List, Dict

try:
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(os.environ.get("GEMINI_MODEL_NAME", "gemini-1.5-flash"))
    else:
        model = None
except ImportError:
    model = None

def extract_pii_with_llm(text: str) -> List[Dict]:
    """
    Use Gemini to identify contextual PII, secrets, or confidential data that standard NER might miss.
    """
    if not model or not os.environ.get("GEMINI_API_KEY"):
        return []

    prompt = f"""
Analyze the following text and extract sensitive information (PII, secrets, passwords, API keys, confidential data).
Return ONLY a JSON object with a single key "violations" containing an array of objects.
Each object must have:
- type: Category of sensitive data (e.g., PASSWORD, API_KEY, FINANCIAL, CONTEXTUAL_LOCATION)
- text: The exact substring from the text
- severity: "HIGH", "MEDIUM", or "LOW"

Text to analyze:
{text}
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        content = response.text
        data = json.loads(content)
        violations = data.get("violations", [])
        
        # Format the violations to match the existing system
        formatted_violations = []
        for v in violations:
            # find start and end
            start_idx = text.find(v.get("text", ""))
            if start_idx != -1:
                end_idx = start_idx + len(v.get("text", ""))
                formatted_violations.append({
                    "type": v.get("type", "LLM_DETECTED"),
                    "text": v.get("text", ""),
                    "start": start_idx,
                    "end": end_idx,
                    "source": "LLM",
                    "confidence": 0.95,
                    "severity": str(v.get("severity", "MEDIUM")).upper()
                })
        return formatted_violations
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return []
