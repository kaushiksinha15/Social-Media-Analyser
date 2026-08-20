# ─────────────────────────────────────────────────────────────────────────────
#  SOCIAL MEDIA CONTENT ANALYZER
#  Hybrid diagnostic engine — Streamlit + Groq AI + textstat
#  Built for Unthink ⚡
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st
import os

from core.ai import get_available_models, analyze_content, adapt_for_platforms
from core.extraction import extract_text
from core.metrics import compute_readability
from ui.components import (
    render_score_ring,
    render_dimension_card,
    render_readability_panel,
    render_strengths_improvements,
    render_platform_tab,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Content Analyzer — Unthink",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Load CSS
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Fallback if CSS is missing

    # ── Session state initialisation ─────────────────────────────────────────
    for key in ("analysis", "platforms", "readability", "input_text"):
        if key not in st.session_state:
            st.session_state[key] = None

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="brand">⚡ Unthink</div>', unsafe_allow_html=True)
        st.markdown('<div class="tagline">Social Media Content Analyzer</div>', unsafe_allow_html=True)

        st.divider()

        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_…",
            help="Get your free key at https://console.groq.com",
        )

        # Dynamic model selector
        selected_model = "llama-3.1-8b-instant"  # safe fallback
        if api_key.strip():
            with st.spinner("Fetching available models…"):
                available_models = get_available_models(api_key.strip())
            if available_models:
                # Prefer larger models at the top of the list
                preferred = [m for m in available_models if "70b" in m or "maverick" in m or "scout" in m]
                rest = [m for m in available_models if m not in preferred]
                ordered = preferred + rest
                selected_model = st.selectbox(
                    "Model",
                    options=ordered,
                    help="All models fetched live from your Groq account",
                )
            else:
                selected_model = st.text_input(
                    "Model ID",
                    value="llama-3.1-8b-instant",
                    help="Could not fetch models. Enter a Groq model ID manually.",
                )

        st.divider()

        st.markdown('<div class="slabel" style="padding:0 0.2rem;">📂 Content Input</div>',
                    unsafe_allow_html=True)

        input_mode = st.radio(
            "Input mode",
            options=["Upload File", "Paste Text"],
            horizontal=True,
            label_visibility="collapsed",
        )

        uploaded_file = None
        raw_text = ""

        if input_mode == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload",
                type=["pdf", "png", "jpg", "jpeg", "webp", "tiff", "txt"],
                label_visibility="collapsed",
            )
        else:
            raw_text = st.text_area(
                "Copy",
                height=210,
                placeholder="Paste your social media copy, ad copy, or marketing text here…",
                label_visibility="collapsed",
            )

        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("⚡ Analyze Content", use_container_width=True)

        st.divider()
        st.markdown("""
        <div style="font-size:0.68rem; color:#25254a; line-height:2;">
            Groq &bull; Llama 3.3 70B &bull; textstat &bull; Tesseract OCR
        </div>
        """, unsafe_allow_html=True)

    # ── Page Header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 2rem 0 0.5rem 0;" class="fade-in">
        <h1 style="
            font-size: 2.3rem;
            font-weight: 900;
            margin: 0 0 0.4rem 0;
            background: linear-gradient(135deg, #ffffff 30%, #a78bfa 70%, #67e8f9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.15;
        ">Content Intelligence Dashboard</h1>
        <p style="color: #35357a; font-size: 0.92rem; margin: 0; font-weight: 500;">
            Multi-dimensional analysis &bull; Hook &bull; CTA &bull; Resonance &bull; Readability &bull; Platform Adaptation
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Analysis Trigger ──────────────────────────────────────────────────────
    if analyze_btn:
        if not api_key.strip():
            st.error("🔑 Please enter your Groq API Key in the sidebar.")
            st.stop()

        input_text = ""
        if uploaded_file is not None:
            with st.spinner("📄 Extracting text from file…"):
                try:
                    input_text = extract_text(uploaded_file)
                except Exception as e:
                    st.error(f"❌ Text extraction failed: {e}")
                    st.stop()
        elif raw_text.strip():
            input_text = raw_text.strip()

        if not input_text:
            st.warning("⚠️ Please upload a file or paste some copy to analyze.")
            st.stop()

        if len(input_text.split()) < 5:
            st.warning("⚠️ Content too short — please provide at least a full sentence.")
            st.stop()

        st.session_state.input_text = input_text

        with st.spinner("🧠 Running AI content analysis…"):
            try:
                st.session_state.analysis = analyze_content(input_text, api_key.strip(), selected_model)
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                st.stop()

        with st.spinner("🌐 Adapting copy for platforms…"):
            try:
                st.session_state.platforms = adapt_for_platforms(input_text, api_key.strip(), selected_model)
            except Exception as e:
                st.error(f"❌ Platform adaptation failed: {e}")
                st.stop()

        with st.spinner("📊 Computing readability metrics…"):
            st.session_state.readability = compute_readability(input_text)

    # ── Results ───────────────────────────────────────────────────────────────
    if st.session_state.analysis and st.session_state.platforms and st.session_state.readability:
        analysis    = st.session_state.analysis
        platforms   = st.session_state.platforms
        readability = st.session_state.readability
        text_preview = st.session_state.input_text or ""

        # ── Row 1: Overall score ring + info panel ─────────────────────────
        col_ring, col_info = st.columns([1, 2.5], gap="large")

        with col_ring:
            render_score_ring(analysis["overall_score"], "Overall Score")

        with col_info:
            st.markdown(f"""
            <div class="card fade-in" style="height:auto; margin-top:0.5rem;">
                <div class="slabel">🎭 Emotional Tone</div>
                <div style="margin-bottom:1.2rem;">
                    <span class="tone-chip">{analysis['emotional_tone']}</span>
                </div>
                <div class="slabel">✂️ Analyzed Copy</div>
                <p style="
                    color: #50508a;
                    font-size: 0.82rem;
                    font-style: italic;
                    line-height: 1.65;
                    margin: 0;
                    max-height: 72px;
                    overflow: hidden;
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical;
                ">"{text_preview[:250]}{'…' if len(text_preview) > 250 else ''}"</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Row 2: Dimension scores ────────────────────────────────────────
        st.markdown('<div class="slabel">📊 Dimension Scores</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            render_dimension_card(
                "🪝", "Hook Retention",
                analysis["hook_score"], analysis["hook_feedback"],
                delay="0s",
            )
        with c2:
            render_dimension_card(
                "📢", "CTA Clarity",
                analysis["cta_score"], analysis["cta_feedback"],
                delay="0.1s",
            )
        with c3:
            render_dimension_card(
                "🎯", "Audience Resonance",
                analysis["audience_resonance_score"], analysis["audience_resonance_feedback"],
                delay="0.2s",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Row 3: Readability ─────────────────────────────────────────────
        render_readability_panel(readability)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Row 4: Strengths & Improvements ───────────────────────────────
        render_strengths_improvements(analysis)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Row 5: Platform Adaptation ────────────────────────────────────
        st.markdown('<div class="slabel">🌐 Platform Adaptation Engine</div>',
                    unsafe_allow_html=True)

        st.markdown("""<div class="card" style="padding:1.6rem 1.6rem 0.8rem;">""",
                    unsafe_allow_html=True)

        tab_li, tab_tw, tab_ig = st.tabs(["💼 LinkedIn", "𝕏 Twitter / X", "📸 Instagram"])

        with tab_li:
            render_platform_tab(platforms["linkedin"], "linkedin")
        with tab_tw:
            render_platform_tab(platforms["twitter"], "twitter")
        with tab_ig:
            render_platform_tab(platforms["instagram"], "instagram")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

    else:
        # ── Empty state ────────────────────────────────────────────────────
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">⚡</div>
            <h2 style="font-size:1.8rem; font-weight:800; color:#ffffff; margin:0 0 0.6rem 0;">
                Ready to analyze
            </h2>
            <p style="color:#30307a; max-width:420px; line-height:1.8; font-size:0.92rem;">
                Upload a <strong style="color:#6050a0;">PDF</strong>,
                <strong style="color:#6050a0;">image</strong>, or paste your copy into the sidebar —
                then hit <strong style="color:#a78bfa;">Analyze Content</strong> to get your
                full content intelligence report.
            </p>
            <div class="feature-grid">
                <div class="feature-pill">🪝 Hook Retention</div>
                <div class="feature-pill">📢 CTA Clarity</div>
                <div class="feature-pill">🎯 Audience Resonance</div>
                <div class="feature-pill">📖 Readability Score</div>
                <div class="feature-pill">💼 LinkedIn</div>
                <div class="feature-pill">𝕏 Twitter / X</div>
                <div class="feature-pill">📸 Instagram</div>
                <div class="feature-pill">🎭 Emotional Tone</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
