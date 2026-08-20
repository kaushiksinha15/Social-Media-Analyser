import streamlit as st

def _score_color(score: int) -> str:
    if score >= 75: return "#34d399"
    if score >= 50: return "#fbbf24"
    return "#f87171"


def _badge_class(score: int) -> str:
    if score >= 75: return "badge-green"
    if score >= 50: return "badge-amber"
    return "badge-red"


def _score_emoji(score: int) -> str:
    if score >= 75: return "✅"
    if score >= 50: return "⚠️"
    return "❌"


def _flesch_label(score: float) -> tuple[str, str]:
    """Return (label, color) for a Flesch Reading Ease score."""
    if score >= 90: return "Very Easy", "#34d399"
    if score >= 80: return "Easy", "#6ee7b7"
    if score >= 70: return "Fairly Easy", "#a7f3d0"
    if score >= 60: return "Standard", "#fbbf24"
    if score >= 50: return "Fairly Difficult", "#fb923c"
    if score >= 30: return "Difficult", "#f87171"
    return "Very Confusing", "#ef4444"


def render_score_ring(score: int, label: str = "Overall Score"):
    color = _score_color(score)
    st.markdown(f"""
    <div class="score-ring-wrapper fade-in">
        <div class="score-ring" style="--score:{score}; --ring-color:{color};">
            <div class="score-ring-gap"></div>
            <div class="score-ring-inner">
                <span class="score-ring-number">{score}</span>
                <span class="score-ring-denom" style="color:{color};">/100</span>
            </div>
        </div>
        <div class="score-ring-title">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_dimension_card(icon: str, label: str, score: int, feedback: str, delay: str = "0s"):
    color = _score_color(score)
    badge_cls = _badge_class(score)
    emoji = _score_emoji(score)
    st.markdown(f"""
    <div class="dim-card" style="animation: fadeInUp 0.5s {delay} ease both; border-top: 3px solid {color}20;">
        <div class="slabel">{icon} {label}</div>
        <div style="margin-bottom:0.9rem;">
            <span class="score-badge {badge_cls}">{emoji}&nbsp;{score}<span style="font-size:0.72rem; opacity:0.6;">/100</span></span>
        </div>
        <p style="color:#70709a; font-size:0.84rem; line-height:1.65; margin:0;">{feedback}</p>
    </div>
    """, unsafe_allow_html=True)


def render_readability_panel(metrics: dict):
    flesch = metrics["flesch_reading_ease"]
    fog    = metrics["gunning_fog"]
    f_label, f_color = _flesch_label(flesch)

    flesch_pct = max(0, min(100, flesch))
    fog_pct    = max(0, min(100, int((1 - min(fog, 20) / 20) * 100)))

    st.markdown("""<div class="card fade-in-1">""", unsafe_allow_html=True)
    st.markdown('<div class="slabel">📖 Readability Analysis</div>', unsafe_allow_html=True)

    # Stat pills
    st.markdown(f"""
    <div class="stat-row" style="margin-bottom:1.4rem;">
        <div class="stat-pill">Words <span>{metrics['word_count']}</span></div>
        <div class="stat-pill">Sentences <span>{metrics['sentence_count']}</span></div>
        <div class="stat-pill">Avg sentence <span>{metrics['avg_sentence_length']} wds</span></div>
        <div class="stat-pill">Syllables <span>{metrics['syllable_count']}</span></div>
        <div class="stat-pill">SMOG Index <span>{metrics['smog_index']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Flesch bar
    st.markdown(f"""
    <div style="margin-bottom:0.3rem;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#8080b0; font-size:0.82rem; font-weight:600;">Flesch Reading Ease</span>
            <span style="color:{f_color}; font-weight:700; font-size:0.88rem;">{flesch} — {f_label}</span>
        </div>
        <div class="rbar-bg">
            <div class="rbar-fill" style="width:{flesch_pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fog bar
    fog_color = "#34d399" if fog <= 8 else "#fbbf24" if fog <= 14 else "#f87171"
    st.markdown(f"""
    <div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#8080b0; font-size:0.82rem; font-weight:600;">
                Gunning Fog Index
                <span style="color:#2a2a6a; font-weight:400;">(lower = more accessible)</span>
            </span>
            <span style="color:{fog_color}; font-weight:700; font-size:0.88rem;">{fog}</span>
        </div>
        <div class="rbar-bg">
            <div class="rbar-fill" style="width:{fog_pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_strengths_improvements(analysis: dict):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="card fade-in-2">""", unsafe_allow_html=True)
        st.markdown('<div class="slabel">💪 Top Strengths</div>', unsafe_allow_html=True)
        for s in analysis.get("top_strengths", []):
            st.markdown(f'<div class="pill-green"><span>✓</span><span>{s}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="card fade-in-3">""", unsafe_allow_html=True)
        st.markdown('<div class="slabel">🔧 Improvements Needed</div>', unsafe_allow_html=True)
        for imp in analysis.get("top_improvements", []):
            st.markdown(f'<div class="pill-amber"><span>→</span><span>{imp}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_platform_tab(platform_data: dict, platform: str):
    colors  = {"linkedin": "#0077b5", "twitter": "#e7e7e7", "instagram": "#e1306c"}
    limits  = {"linkedin": 1300, "twitter": 280, "instagram": 2200}
    icons   = {"linkedin": "💼", "twitter": "𝕏", "instagram": "📸"}

    copy       = platform_data.get("copy", "")
    hashtags   = platform_data.get("hashtags", [])
    char_count = platform_data.get("character_count", len(copy))
    limit      = limits.get(platform, 2200)
    color      = colors.get(platform, "#7c3aed")
    icon       = icons.get(platform, "📱")
    over       = char_count > limit

    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.9rem;">
        <span style="font-size:1.05rem; font-weight:700; color:#e0e0f0;">{icon} {platform.capitalize()} Copy</span>
        <span style="font-size:0.78rem; font-weight:700;
            color:{'#f87171' if over else '#34d399'};
            background:{'#2a0b0b' if over else '#0b2318'};
            padding:3px 10px; border-radius:999px; border:1px solid {'#f8717130' if over else '#34d39930'};">
            {char_count:,} / {limit:,} chars {'⚠️' if over else '✓'}
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.code(copy, language=None)

    if hashtags:
        tag_str = "  ".join(f"#{h.strip().lstrip('#')}" for h in hashtags)
        st.markdown(f"""
        <div class="hashtag-block">
            <span class="htag-label">Hashtags</span>
            <span style="color:{color}; font-size:0.88rem; font-weight:600; line-height:1.8;">{tag_str}</span>
        </div>
        """, unsafe_allow_html=True)
