import json
import re
import streamlit as st
from groq import Groq
from .prompts import ANALYSIS_PROMPT, PLATFORM_PROMPT


@st.cache_data(ttl=300, show_spinner=False)
def get_available_models(api_key: str) -> list[str]:
    """Fetch currently-active models from the Groq API (cached 5 min)."""
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        # Filter to text-generation models (exclude whisper/tts)
        ids = [
            m.id for m in models.data
            if not any(x in m.id for x in ["whisper", "tts", "guard", "vision"])
        ]
        return sorted(ids)
    except Exception:
        return []


def _extract_json(text: str) -> dict:
    """Robustly extract a JSON object from a model response string."""
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strip markdown code fences
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if match:
        return json.loads(match.group(1))
    # Last resort: find first { ... }
    match = re.search(r"(\{[\s\S]+\})", text)
    if match:
        return json.loads(match.group(1))
    raise ValueError(f"No valid JSON found in model response: {text[:200]}")


def analyze_content(text: str, api_key: str, model: str) -> dict:
    """Run multi-dimensional content analysis via Groq."""
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": '''You are an expert social media strategist. Always respond with valid JSON only — no prose, no markdown fences. 
You MUST return a JSON object with this exact schema:
{
  "hook_score": <int 0-100>,
  "hook_feedback": "<string>",
  "cta_score": <int 0-100>,
  "cta_feedback": "<string>",
  "audience_resonance_score": <int 0-100>,
  "audience_resonance_feedback": "<string>",
  "overall_score": <int 0-100>,
  "top_strengths": ["<string>", "<string>", "<string>"],
  "top_improvements": ["<string>", "<string>", "<string>"],
  "emotional_tone": "<string>"
}'''},
            {"role": "user",   "content": ANALYSIS_PROMPT.format(text=text)},
        ],
        response_format={"type": "json_object"},
        temperature=0.25,
    )
    return _extract_json(response.choices[0].message.content)


def adapt_for_platforms(text: str, api_key: str, model: str) -> dict:
    """Refactor copy into LinkedIn, Twitter, and Instagram native formats via Groq."""
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": '''You are a platform-native copywriter. Always respond with valid JSON only — no prose, no markdown fences.
You MUST return a JSON object with this exact schema:
{
  "linkedin": { "copy": "<string>", "hashtags": ["<string>"], "character_count": <int> },
  "twitter": { "copy": "<string>", "hashtags": ["<string>"], "character_count": <int> },
  "instagram": { "copy": "<string>", "hashtags": ["<string>"], "character_count": <int> }
}'''},
            {"role": "user",   "content": PLATFORM_PROMPT.format(text=text)},
        ],
        response_format={"type": "json_object"},
        temperature=0.6,
    )
    return _extract_json(response.choices[0].message.content)
