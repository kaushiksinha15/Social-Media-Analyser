ANALYSIS_PROMPT = """You are a world-class social media strategist and direct-response copywriter.

Perform a rigorous multi-dimensional evaluation of the following social media copy.

Scoring rubric (0–100):
- hook_score: Does the opening create immediate curiosity, urgency, or emotional pull? Is it scroll-stopping?
- cta_score: Is there a clear, specific, benefit-driven call-to-action? Is friction minimised?
- audience_resonance_score: Does the language, tone, and message match the likely target audience? Does it feel native to the platform?
- overall_score: Weighted holistic quality (hook 30%, CTA 30%, resonance 30%, prose quality 10%).

Requirements:
- top_strengths: exactly 3 specific, concrete strengths (not generic)
- top_improvements: exactly 3 specific, actionable improvements with clear rationale
- emotional_tone: concise phrase describing dominant emotional register (e.g. "Aspirational & Direct" or "Playful & Curious")

CONTENT:
---
{text}
---"""

PLATFORM_PROMPT = """You are a senior platform-native copywriter.

Adapt the content below into three platform-optimised versions. Preserve the core message but reformat completely for each platform's native conventions.

Platform requirements:
- linkedin: Professional tone, 800–1300 chars, strategic use of line breaks and white space, conversational yet authoritative, 3–5 niche-relevant hashtags placed at end
- twitter: Max 260 chars (copy only, not counting hashtags), punchy one-liner or 2-line max, conversational, includes a hook or insight, 1–2 hashtags
- instagram: Visual-first storytelling, 150–400 chars before hashtag block, strategic emoji use (2–4), line breaks, curiosity gap or narrative, 8–12 hashtags as separate block

Set character_count to the byte length of the copy field only (not including hashtags array content).

IMPORTANT: You MUST output ONLY valid JSON. No conversational text, no markdown fences, no explanations. 

ORIGINAL COPY:
---
{text}
---"""
