import streamlit as st
from connect_llm_with_memory import answer_question, embedding_model, db


@st.cache_resource
def get_cached_embedding_model():
    return embedding_model


@st.cache_resource
def get_cached_vector_db():
    return db


@st.cache_data
def cached_answer_question(question):
    return answer_question(question)


# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="MedChat",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Premium CSS ────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ───────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ────────────────────────────── */
:root {
    --bg-primary: #0a0f1a;
    --bg-secondary: #111827;
    --bg-card: #1a2332;
    --accent: #6366f1;
    --accent-hover: #818cf8;
    --accent-glow: rgba(99, 102, 241, 0.25);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: rgba(148, 163, 184, 0.1);
    --success: #10b981;
    --warning: #f59e0b;
}

/* ── Global ────────────────────────────────────── */
*, html, body { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit boilerplate ────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─────────────────────────────────────────────────
   SIDEBAR
   ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span {
    color: var(--text-secondary) !important;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(99, 102, 241, 0.08) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    color: var(--accent-hover) !important;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    font-weight: 500;
    transition: all 0.25s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99, 102, 241, 0.15) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 16px var(--accent-glow);
}

/* ── Main title ────────────────────────────────── */
h1 {
    background: linear-gradient(135deg, #6366f1, #a78bfa, #6366f1);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    animation: gradient-shift 4s ease infinite;
    text-align: center !important;
}

@keyframes gradient-shift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ─────────────────────────────────────────────────
   CHAT MESSAGES — FIX AVATAR OVERLAP
   ───────────────────────────────────────────────── */

/* Message card */
div[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.8rem !important;
    gap: 0.8rem !important;
    animation: msg-in 0.3s ease-out;
}

div[data-testid="stChatMessage"]:hover {
    border-color: rgba(99, 102, 241, 0.15) !important;
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.15);
}

@keyframes msg-in {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Text inside messages */
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] em,
div[data-testid="stChatMessage"] strong {
    color: var(--text-primary) !important;
    line-height: 1.65 !important;
    font-size: 0.92rem !important;
}

/* ── AVATAR FIX ─────────────────────────────────
   Streamlit renders Material Icon names as raw text
   (e.g. "smart_toy"). Hide that text and replace
   with emoji-style avatars via CSS.
   ────────────────────────────────────────────────── */

/* Avatar containers — fixed size, no overflow */
div[data-testid="stChatMessageAvatarUser"],
div[data-testid="stChatMessageAvatarAssistant"] {
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    border-radius: 10px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden !important;
    font-size: 0px !important;          /* hide raw icon text */
    flex-shrink: 0 !important;
}

/* Hide the Material Icon text span */
div[data-testid="stChatMessageAvatarUser"] span[data-testid="stIconMaterial"],
div[data-testid="stChatMessageAvatarAssistant"] span[data-testid="stIconMaterial"] {
    font-size: 0px !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* Assistant avatar */
div[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
}

div[data-testid="stChatMessageAvatarAssistant"]::after {
    content: "🩺";
    font-size: 18px;
    display: block;
}

/* User avatar */
div[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #0ea5e9, #06b6d4) !important;
}

div[data-testid="stChatMessageAvatarUser"]::after {
    content: "👤";
    font-size: 18px;
    display: block;
}

/* ─────────────────────────────────────────────────
   CHAT INPUT — DARK THEMED
   ───────────────────────────────────────────────── */
.stChatInput,
div[data-testid="stChatInput"] {
    background: var(--bg-primary) !important;
    border-top: 1px solid var(--border) !important;
    padding: 0.5rem 0 !important;
}

div[data-testid="stChatInput"] > div {
    background: var(--bg-card) !important;
    border: 1px solid rgba(148, 163, 184, 0.15) !important;
    border-radius: 12px !important;
}

div[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-glow) !important;
}

div[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    caret-color: var(--accent) !important;
    background: transparent !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

div[data-testid="stChatInput"] button {
    color: var(--accent) !important;
    background: transparent !important;
}

div[data-testid="stChatInput"] button:hover {
    color: var(--accent-hover) !important;
}

/* ── Bottom bar background fix ─────────────────── */
/* Aggressively target ALL bottom containers */
.stBottom,
div[data-testid="stBottom"],
div[data-testid="stBottomBlockContainer"],
div[data-testid="stBottom"] > div,
div[data-testid="stBottomBlockContainer"] > div,
.stChatFloatingInputContainer,
[class*="stBottom"],
[class*="bottom"] {
    background: #0a0f1a !important;
    background-color: #0a0f1a !important;
}

/* Force chat input wrapper backgrounds */
.stChatInput,
.stChatInput > *,
.stChatInput > div,
.stChatInput > div > *,
.stChatInput > div > div,
.stChatInput > div > div > *,
div[data-testid="stChatInput"],
div[data-testid="stChatInput"] > *,
div[data-testid="stChatInput"] > div,
div[data-testid="stChatInput"] > div > *,
div[data-testid="stChatInput"] > div > div {
    background: #1a2332 !important;
    background-color: #1a2332 !important;
}

/* Force the textarea itself */
.stChatInput textarea,
div[data-testid="stChatInput"] textarea,
textarea[data-testid="stChatInputTextArea"] {
    background: #1a2332 !important;
    background-color: #1a2332 !important;
    color: #f1f5f9 !important;
    caret-color: #6366f1 !important;
    border: none !important;
}

textarea[data-testid="stChatInputTextArea"]::placeholder {
    color: #64748b !important;
}

/* Submit button */
button[data-testid="stChatInputSubmitButton"],
button[data-testid="stChatInputSubmitButton"] > * {
    background: transparent !important;
    color: #6366f1 !important;
}

/* ── Spinner ───────────────────────────────────── */
.stSpinner > div { border-top-color: var(--accent) !important; }
.stSpinner p { color: var(--text-secondary) !important; }

/* ── Error messages ────────────────────────────── */
.stAlert {
    background: rgba(239, 68, 68, 0.08) !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}

/* ── Scrollbar ─────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

/* ── Dividers ──────────────────────────────────── */
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 0.5rem;">
        <div style="font-size: 2.8rem; margin-bottom: 0.2rem;">🩺</div>
        <h2 style="
            background: linear-gradient(135deg, #6366f1, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            margin: 0;
            font-size: 1.6rem;
        ">MedChat</h2>
        <p style="color: #64748b; font-size: 0.78rem; margin-top: 2px;">
            Evidence-Based Medical AI
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <p style="color:#94a3b8; font-size:0.82rem; line-height:1.65;">
        MedChat retrieves answers <b style="color:#e2e8f0;">strictly</b> from verified medical
        documents. It does not guess, diagnose, or prescribe.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:0.6rem;">
        <p style="color:#64748b; font-size:0.7rem; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:0.3rem;">
            Guidelines
        </p>
        <ul style="color:#94a3b8; font-size:0.78rem; line-height:1.85; padding-left:1.2rem; margin:0;">
            <li>Answers from documentation only</li>
            <li>No personal diagnosis or treatment</li>
            <li>Educational purposes only</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="
        background: rgba(245, 158, 11, 0.06);
        border: 1px solid rgba(245, 158, 11, 0.12);
        border-radius: 10px;
        padding: 0.7rem 0.8rem;
    ">
        <p style="color:#f59e0b; font-size:0.7rem; font-weight:700; margin:0 0 3px;">
            ⚠️ DISCLAIMER
        </p>
        <p style="color:#94a3b8; font-size:0.72rem; line-height:1.5; margin:0;">
            Not a substitute for professional medical advice.
            In emergencies, call <b style="color:#f1f5f9;">911</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")  # spacer

    if st.button("🗑  Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


# ─── Main ───────────────────────────────────────────────────────
st.markdown("<h1>🩺 MedChat</h1>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center; color:#64748b; font-size:0.85rem; margin-top:-0.6rem; margin-bottom:1.5rem;">
    Your AI-powered medical knowledge assistant
</p>
""", unsafe_allow_html=True)


# ─── Session ────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Welcome to **MedChat**!\n\n"
                "I can help you find evidence-based medical information from verified documents. "
                "Ask me anything about symptoms, conditions, treatments, or medications.\n\n"
                "*Remember: I provide educational information only — not medical advice.*"
            ),
        }
    ]

_ = get_cached_embedding_model()
_ = get_cached_vector_db()

# ─── Chat History ───────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── Input ──────────────────────────────────────────────────────
prompt = st.chat_input("Ask a medical question...")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("🔍 Searching medical records..."):
        try:
            response = cached_answer_question(prompt)
        except Exception as e:
            error_msg = str(e)
            if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
                response = (
                    "⚠️ **Rate limit reached.** The AI model's free quota has been temporarily "
                    "exceeded. Please wait a minute and try again."
                )
            elif "NOT_FOUND" in error_msg or "404" in error_msg:
                response = (
                    "⚠️ **Model not available.** The configured AI model could not be found. "
                    "Please check the model name in `connect_llm_with_memory.py`."
                )
            else:
                response = (
                    f"⚠️ **Something went wrong.** An error occurred while processing your request.\n\n"
                    f"*Error: {error_msg[:200]}*"
                )

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
