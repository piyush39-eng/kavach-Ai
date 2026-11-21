import os
import tempfile
import streamlit as st
from PIL import Image, ExifTags
from groq import Groq

@st.cache_resource
def get_ocr_reader():
   """Load OCR only when needed and reuse it across Streamlit reruns."""
   try:
    import easyocr
   except ImportError:
    return None
   return easyocr.Reader(["en", "hi"], gpu=False)

# 1. Page Configuration
st.set_page_config(
    page_title="Kavach AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ChatGPT-Style Dark UI CSS
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(ellipse at 50% -20%, rgba(35, 101, 95, 0.18), transparent 55%),
            #101716;
        color: #E8F0ED;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    header[data-testid="stHeader"] { background-color: rgba(16, 23, 22, 0.82); }
    #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1040px; padding-top: 2rem; padding-bottom: 5rem; }

    section[data-testid="stSidebar"] {
        background-color: #131C1A;
        border-right: 1px solid #273633;
    }
    section[data-testid="stSidebar"] * { color: #E8F0ED !important; }

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse;
        background-color: transparent;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-testid="stChatMessageContent"] {
        background-color: #1D2A27;
        color: #E8F0ED;
        border: 1px solid #2A3B37;
        border-radius: 18px;
        padding: 12px 18px;
        max-width: 82%;
        margin-left: auto;
    }

    .stButton > button {
        min-height: 3.2rem;
        background-color: #192522;
        color: #E8F0ED;
        border: 1px solid #30443F;
        border-radius: 14px;
        padding: 12px 16px;
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #22332F;
        border-color: #4B766A;
        color: #FFFFFF;
    }

    div[data-testid="stChatInput"] { background-color: #101716; }
    div[data-testid="stChatInput"] > div {
        background-color: #1A2623 !important;
        border: 1px solid #38514A !important;
        border-radius: 26px !important;
        padding: 4px 10px;
    }
    div[data-testid="stChatInput"] textarea { color: #E8F0ED !important; }
    .kavach-eyebrow {
        color: #78C7A7;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }
    .kavach-note {
        color: #A7B8B2;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Groq API Setup
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        groq_api_key = None

if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Set it as an environment variable or in .streamlit/secrets.toml.")
    st.stop()

client = Groq(api_key=groq_api_key)

# 4. System Prompt
SYSTEM_PROMPT = """
You are Kavach AI, a ChatGPT-style AI assistant specializing in Cyber Safety, Scam Prevention, AI-Generated Media Forensics, and Deepfake Detection.

HOW TO RESPOND:
1. Always reply in clear, natural English, regardless of the user's language.
2. FORENSIC CHECK: When the user shares a message, URL, screenshot text, photo metadata, or video audio transcript, inspect it carefully and reply in this structured format:

**🛡️ Verdict:** [SAFE / SUSPICIOUS / HIGH-RISK / INCONCLUSIVE]  
**📊 Estimated Risk Score:** [0–100]%  
**🔍 Category:** [e.g., UPI Scam / Phishing Link / Fake Payment Screenshot / Voice Scam / Genuine]

**🚩 Key Clues Found:**
- [Clue 1: Specific red flag from text, metadata, or audio]
- [Clue 2: Specific clue]

**✅ What You Should Do:**
- [Action step 1]
- [Action step 2]

Do not treat missing metadata or a single video frame as proof. Explain uncertainty and use INCONCLUSIVE when the available evidence is insufficient.
"""

# 5. Helper Functions
def analyze_image_forensics(image_path: str) -> str:
    """Extracts EXIF camera metadata + OCR text from images/screenshots."""
    details = []
    with Image.open(image_path) as img:
        details.append(f"Resolution: {img.size[0]}x{img.size[1]}, Format: {img.format}")
        exif = img.getexif()
        if not exif:
            details.append("EXIF Metadata: Not found; this alone does not establish whether an image is genuine or edited.")
        else:
            tags = [
                f"{ExifTags.TAGS.get(k, k)}: {v}"
                for k, v in exif.items()
                if ExifTags.TAGS.get(k, k) in ["Make", "Model", "Software"]
            ]
            details.append("EXIF Metadata: " + (", ".join(tags) if tags else "Camera model tags not found"))

    reader = get_ocr_reader()
    if reader is None:
        details.append("OCR: Unavailable; install easyocr to extract text from this image.")
    else:
        text_lines = reader.readtext(image_path, detail=0)
        extracted_text = " ".join(text_lines).strip()
        details.append(f"Extracted Text inside Image (OCR): {extracted_text if extracted_text else 'No readable text found'}")

    return "\n".join(details)

def transcribe_video_audio(video_path: str) -> str:
    """Uses Groq Whisper model to transcribe speech from uploaded video/audio."""
    try:
        with open(video_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(video_path), f.read()),
                model="whisper-large-v3-turbo",
                response_format="text"
            )
        return f"Video Audio Transcript: {transcription.strip()}"
    except Exception as e:
        raise RuntimeError(f"Could not transcribe speech from the video: {e}") from e

# 6. Sidebar
with st.sidebar:
    st.markdown("### 🛡️ Kavach AI")
    if st.button("✏️  New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.quick_prompt = None
        st.rerun()
    st.markdown("---")
    st.caption("Active Capabilities:")
    st.markdown(
        "📩 **Scam SMS / Links**\n\n"
        "💳 **Fake UPI Screenshot OCR**\n\n"
        "🖼️ **Photo Metadata Forensics**\n\n"
        "🎥 **Video Voice Scam Check**"
    )

# 7. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

# 8. Welcome Screen
if len(st.session_state.messages) == 0:
    st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='kavach-eyebrow' style='text-align: center;'>Your digital safety companion</p>"
        "<h1 style='text-align: center; font-weight: 700; font-size: clamp(2.2rem, 5vw, 3.2rem); margin: 0.25rem 0;'>"
        "🛡️ Kavach AI</h1>"
        "<p style='text-align: center; color: #B5C4BF; font-size: 1.05rem; max-width: 680px; "
        "margin: 0 auto 1.5rem;'>Check suspicious messages, links, screenshots, and videos with clear, "
        "evidence-based guidance.</p>"
        "<p class='kavach-note'>AI assessments can be uncertain. Never share passwords, OTPs, or financial details.</p>",
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📩 Check a suspicious SMS or link", use_container_width=True):
            st.session_state.quick_prompt = "I received a suspicious SMS. How can I tell if it is a scam?"
            st.rerun()
        if st.button("🎥 How to spot a deepfake video", use_container_width=True):
            st.session_state.quick_prompt = "How can I recognize a deepfake face-swap video?"
            st.rerun()
    with col2:
        if st.button("🖼️ Check an AI-generated photo", use_container_width=True):
            st.session_state.quick_prompt = "How can I tell an AI-generated photo from a real photo?"
            st.rerun()
        if st.button("🚨 What is a digital arrest scam?", use_container_width=True):
            st.session_state.quick_prompt = "What is a digital arrest scam, and how can I protect myself?"
            st.rerun()

# 9. Display Chat History
for msg in st.session_state.messages:
    avatar = "🛡️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("media_name"):
            st.caption(f"📎 {msg['media_name']}")

# 10. Unified Chat Input
user_input = st.chat_input(
    "Message Kavach AI or attach a screenshot/video...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "webp", "mp4", "mov"]
)

active_text = None
uploaded_file = None

if user_input:
    active_text = user_input.text or ""
    if user_input.files:
        uploaded_file = user_input.files[0]
elif st.session_state.quick_prompt:
    active_text = st.session_state.quick_prompt
    st.session_state.quick_prompt = None

# 11. Generate Response Using Your Active Groq Models
if active_text is not None or uploaded_file is not None:
    display_text = active_text if active_text else "Check this file (real vs. fake/scam):"
    media_label = uploaded_file.name if uploaded_file else None

    st.session_state.messages.append({
        "role": "user",
        "content": display_text,
        "media_name": media_label
    })

    with st.chat_message("user", avatar="👤"):
        if active_text:
            st.markdown(active_text)
        if uploaded_file:
            if uploaded_file.type.startswith("image/"):
                st.image(uploaded_file, width=260)
            else:
                st.video(uploaded_file)

    with st.chat_message("assistant", avatar="🛡️"):
        try:
            api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for m in st.session_state.messages[-6:-1]:
                api_messages.append({"role": m["role"], "content": m["content"]})

            final_user_prompt = display_text

            if uploaded_file:
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    temp_path = tmp.name

                try:
                    if uploaded_file.type.startswith("image/"):
                        forensics_report = analyze_image_forensics(temp_path)
                    else:
                        forensics_report = transcribe_video_audio(temp_path)
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                final_user_prompt = (
                    f"{display_text}\n\n"
                    f"--- EXTRACTED FILE FORENSICS ({uploaded_file.name}) ---\n"
                    f"{forensics_report}"
                )

            api_messages.append({"role": "user", "content": final_user_prompt})

            def stream_reply():
                stream = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=api_messages,
                    temperature=0.3,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta

            full_reply = st.write_stream(stream_reply())
            st.session_state.messages.append({"role": "assistant", "content": full_reply})

        except Exception as e:
            st.error(f"Error: {str(e)}")