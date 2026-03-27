import streamlit as st
import connect_llm_with_memory as llm_handler
import re

st.set_page_config(
    page_title="MedChat",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #EEF2F7 !important;
    color: #1E293B !important;
}

/* Hide Streamlit chrome */
#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* ─────────────── SIDEBAR ─────────────── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #DDE3ED !important;
    min-width: 255px !important;
    max-width: 255px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* Logo area */
.sb-top {
    padding: 22px 20px 16px;
    border-bottom: 1px solid #EEF2F7;
}
.sb-brand {
    font-size: 22px;
    font-weight: 700;
    color: #0A2540;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sb-brand-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: linear-gradient(135deg, #00C9A7, #0066FF);
    display: inline-block;
}
.sb-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    margin-top: 10px;
    background: #0A2540;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
    border-radius: 6px;
    padding: 5px 11px;
}

/* Section label */
.sb-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    color: #94A3B8;
    padding: 16px 20px 6px;
}

/* Quick-query buttons — scoped to sidebar */
section[data-testid="stSidebar"] [data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid #E2E8F0 !important;
    color: #334155 !important;
    padding: 8px 14px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    min-height: 38px !important;
    height: auto !important;
    box-shadow: none !important;
    border-radius: 8px !important;
    width: calc(100% - 32px) !important;
    margin: 3px 16px !important;
    transition: all 0.15s !important;
    display: block !important;
}
section[data-testid="stSidebar"] [data-testid="stButton"] button:hover {
    background: #F0F7FF !important;
    border-color: #93C5FD !important;
    color: #1D4ED8 !important;
}
section[data-testid="stSidebar"] [data-testid="stButton"] button p {
    font-size: 13px !important;
    margin: 0 !important;
    font-weight: 400 !important;
    text-align: left !important;
}

/* Disclaimer */
.sb-disclaimer {
    margin: 16px 16px 10px;
    background: #FFFBEB;
    border-left: 3px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 10px 12px;
    font-size: 11.5px;
    color: #78350F;
    line-height: 1.55;
}

/* New session button */
.sb-new-btn {
    padding: 4px 16px 20px;
}
.sb-new-btn [data-testid="stButton"] button {
    background: #F8FAFC !important;
    border: 1px solid #CBD5E1 !important;
    color: #374151 !important;
    border-radius: 8px !important;
    padding: 9px 16px !important;
    width: 100% !important;
    justify-content: center !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06) !important;
    margin: 0 !important;
}
.sb-new-btn [data-testid="stButton"] button:hover {
    background: #EFF6FF !important;
    border-color: #93C5FD !important;
    color: #1D4ED8 !important;
}

/* ─────────────── MAIN CONTENT ─────────────── */
.main .block-container {
    max-width: 820px;
    padding: 0 2rem 7rem 2rem;
    margin: 0 auto;
}

/* Top bar */
.topbar {
    padding: 24px 0 16px;
    margin-bottom: 8px;
}
.topbar-title {
    font-size: 22px;
    font-weight: 700;
    color: #0A2540;
    letter-spacing: -0.3px;
}
.topbar-sub {
    font-size: 13px;
    color: #94A3B8;
    margin-top: 3px;
}
.topbar-divider {
    height: 1px;
    background: linear-gradient(90deg, #CBD5E1 0%, transparent 80%);
    margin-top: 14px;
}

/* ── User bubble ── */
.user-row {
    display: flex;
    justify-content: flex-end;
    margin: 0 0 18px;
}
.user-bubble {
    background: linear-gradient(135deg, #0066FF 0%, #0047B3 100%);
    color: #FFFFFF;
    border-radius: 18px 18px 4px 18px;
    padding: 11px 18px;
    font-size: 14.5px;
    line-height: 1.6;
    max-width: 68%;
    box-shadow: 0 4px 16px rgba(0,102,255,0.22);
}

/* ── AI card ── */
.ai-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    margin-bottom: 24px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
}
.ai-card-header {
    padding: 12px 18px;
    background: #F8FAFC;
    border-bottom: 1px solid #E2E8F0;
    display: flex;
    align-items: center;
    gap: 9px;
}
.ai-header-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: linear-gradient(135deg, #00C9A7, #0066FF);
}
.ai-header-name {
    font-size: 12px;
    font-weight: 600;
    color: #64748B;
    letter-spacing: 0.2px;
}
.ai-card-body {
    padding: 18px 20px 20px;
}
.ai-answer {
    font-size: 14.5px;
    color: #1E293B;
    line-height: 1.72;
}

/* Sections inside AI card */
.ai-section {
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid #F1F5F9;
}
.sec-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.9px;
    text-transform: uppercase;
    border-radius: 4px;
    padding: 2px 8px;
    margin-bottom: 8px;
}
.tag-green { background: #DCFCE7; color: #166534; }
.tag-amber { background: #FEF3C7; color: #92400E; }
.tag-slate { background: #F1F5F9; color: #475569; }
.tag-blue  { background: #DBEAFE; color: #1E40AF; }

.ev-list {
    margin: 0 0 0 16px;
    padding: 0;
    font-size: 13.5px;
    color: #334155;
    line-height: 1.75;
}
.ev-list li { margin-bottom: 3px; }

.lim-text {
    font-size: 13.5px;
    color: #374151;
    line-height: 1.65;
    margin: 0;
}

.conf-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    font-weight: 600;
    border-radius: 999px;
    padding: 4px 14px;
}
.c-high   { background: #DCFCE7; color: #15803D; border: 1px solid #86EFAC; }
.c-medium { background: #FEF9C3; color: #A16207; border: 1px solid #FDE047; }
.c-low    { background: #FEE2E2; color: #B91C1C; border: 1px solid #FCA5A5; }

.src-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.src-chip {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 5px;
    padding: 3px 10px;
    font-size: 11.5px;
    color: #475569;
}

/* ── Welcome screen ── */
.welcome {
    text-align: center;
    padding: 56px 16px 32px;
}
.wlc-circle {
    width: 68px; height: 68px;
    background: linear-gradient(135deg, #00C9A7 0%, #0066FF 100%);
    border-radius: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; color: #fff;
    margin: 0 auto 18px;
    box-shadow: 0 8px 24px rgba(0,102,255,0.18);
}
.wlc-title { font-size: 23px; font-weight: 700; color: #0A2540; margin-bottom: 10px; }
.wlc-sub {
    font-size: 14.5px; color: #64748B;
    max-width: 460px; margin: 0 auto 28px; line-height: 1.65;
}
.wlc-features {
    display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
}
.wlc-feat {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 9px;
    padding: 9px 16px;
    font-size: 13px;
    color: #374151;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* Footer */
.page-footer {
    position: fixed; bottom: 0;
    left: 255px; right: 0;
    background: rgba(238,242,247,0.95);
    backdrop-filter: blur(8px);
    border-top: 1px solid #DDE3ED;
    padding: 6px 0 5px;
    font-size: 11px;
    color: #94A3B8;
    text-align: center;
    z-index: 999;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def conf_class(level):
    return {"high": "c-high", "moderate": "c-medium", "medium": "c-medium", "low": "c-low"}.get(
        level.lower(), "c-medium"
    )


def format_ai_response(text):
    parts = re.split(
        r"(Supporting Evidence:|Limitations:|Confidence:|Sources:)",
        text,
        flags=re.IGNORECASE,
    )

    answer_parts = []
    evidence_items = []
    limitations_parts = []
    confidence_level = ""
    source_items = []
    current = "answer"

    for part in parts:
        stripped = part.strip()
        if not stripped:
            continue
        low = stripped.lower()

        if low in ("supporting evidence:", "limitations:", "confidence:", "sources:"):
            if "supporting evidence" in low:
                current = "evidence"
            elif "limitations" in low:
                current = "limitations"
            elif "confidence" in low:
                current = "confidence"
            elif "sources" in low:
                current = "sources"
        else:
            if current == "answer":
                answer_parts.append(part)
            elif current == "evidence":
                evidence_items += [
                    ln.strip().lstrip("-•* ").strip()
                    for ln in part.split("\n")
                    if ln.strip().lstrip("-•* ").strip()
                ]
            elif current == "limitations":
                limitations_parts.append(stripped.lstrip("-•* ").strip())
            elif current == "confidence":
                m = re.search(r"(High|Moderate|Medium|Low)", part, re.IGNORECASE)
                if m:
                    confidence_level = m.group(1).capitalize()
            elif current == "sources":
                source_items += [
                    ln.strip().lstrip("-•* ").strip()
                    for ln in part.split("\n")
                    if ln.strip().lstrip("-•* ").strip()
                ]

    answer = " ".join(answer_parts).strip()
    answer = re.sub(r"^(clinical answer:|answer:)\s*", "", answer, flags=re.IGNORECASE).strip()
    answer = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", answer)

    h = '<div class="ai-card">'
    h += (
        '<div class="ai-card-header">'
        '<div class="ai-header-dot"></div>'
        '<span class="ai-header-name">MedChat &nbsp;·&nbsp; AI Medical Assistant</span>'
        '</div>'
    )
    h += f'<div class="ai-card-body"><div class="ai-answer">{answer}</div>'

    # Evidence
    h += '<div class="ai-section"><span class="sec-tag tag-green">📋 Supporting Evidence</span>'
    if evidence_items:
        h += '<ul class="ev-list">' + "".join(f"<li>{e}</li>" for e in evidence_items) + "</ul>"
    else:
        h += '<p style="font-size:13px;color:#94A3B8;margin:0;">No direct quotes extracted.</p>'
    h += "</div>"

    if limitations_parts:
        h += '<div class="ai-section"><span class="sec-tag tag-amber">⚠ Limitations</span>'
        h += f'<p class="lim-text">{" ".join(limitations_parts)}</p></div>'

    if confidence_level:
        cls = conf_class(confidence_level)
        h += '<div class="ai-section"><span class="sec-tag tag-slate">Confidence</span><br>'
        h += f'<span class="conf-badge {cls}">{confidence_level}</span></div>'

    if source_items:
        h += '<div class="ai-section"><span class="sec-tag tag-blue">📚 Sources</span>'
        h += '<div class="src-row">' + "".join(f'<span class="src-chip">{s}</span>' for s in source_items) + "</div>"
        h += "</div>"

    h += "</div></div>"
    return h


# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_to_submit" not in st.session_state:
    st.session_state.query_to_submit = None


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown(
        '<div class="sb-top">'
        '<div class="sb-brand">'
        '<div class="sb-brand-dot"></div>MedChat'
        '</div>'
        '<div class="sb-pill">⚡ Powered by OpenAI GPT-4o + RAG</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sb-label">Example Queries</div>', unsafe_allow_html=True)

    quick = [
        "What causes migraines?",
        "How is diabetes managed?",
        "Symptoms of heart failure",
        "What is asthma?",
        "How does ibuprofen work?",
    ]
    for q in quick:
        if st.button(q, key=f"q_{q[:14]}"):
            st.session_state.query_to_submit = q

    st.markdown(
        '<div class="sb-disclaimer">'
        '⚠️ Not a substitute for professional medical advice. '
        'In emergencies, call <strong>911</strong>.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sb-new-btn">', unsafe_allow_html=True)
    if st.button("🔄  New Session", use_container_width=True, key="reset_btn"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.messages:
        n = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(
            f'<div style="text-align:center;font-size:11px;color:#CBD5E1;padding:4px 0 16px;">'
            f'{n} question{"s" if n != 1 else ""} this session'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── MAIN AREA ──────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="topbar">'
    '<div class="topbar-title">Medical Assistant</div>'
    '<div class="topbar-sub">Evidence-based answers grounded in verified medical literature</div>'
    '<div class="topbar-divider"></div>'
    '</div>',
    unsafe_allow_html=True,
)

# Welcome screen
if not st.session_state.messages:
    st.markdown(
        '<div class="welcome">'
        '<div class="wlc-circle">⚕</div>'
        '<div class="wlc-title">How can I help you today?</div>'
        '<div class="wlc-sub">'
        "Ask any medical question. I'll search peer-reviewed literature and return "
        "evidence-backed answers with sources, confidence levels, and known limitations."
        "</div>"
        '<div class="wlc-features">'
        '<div class="wlc-feat">📋 Evidence-backed answers</div>'
        '<div class="wlc-feat">🔍 RAG-powered search</div>'
        '<div class="wlc-feat">📚 Cited sources</div>'
        '<div class="wlc-feat">⚠️ Transparent limitations</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )

# Chat history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(msg["html"], unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="user-row"><div class="user-bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True,
        )

# Sticky footer
st.markdown(
    '<div class="page-footer">'
    "MedChat uses RAG over verified medical documents · Not a substitute for professional advice"
    "</div>",
    unsafe_allow_html=True,
)

# ── Input ──────────────────────────────────────────────────────────────────────
query = st.chat_input("Ask a medical question…")

if st.session_state.query_to_submit:
    query = st.session_state.query_to_submit
    st.session_state.query_to_submit = None

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("Searching medical literature…"):
        try:
            resp = llm_handler.answer_question(st.session_state.messages[-1]["content"])
            st.session_state.messages.append({
                "role": "assistant",
                "content": resp,
                "html": format_ai_response(resp),
            })
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
