import streamlit as st
import requests
import base64

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="NxT AI", layout="wide", page_icon="❄️")
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #FFFFFF;
    }

    .stApp {
        background-color: #1e1e1e;
        color: #FFFFFF;
    }

    header[data-testid="stHeader"] {
        background-color: #1e1e1e;
        color: white;
        border-bottom: 1px solid #333;
    }

    [data-testid="stSidebarNav"] {
        background-color: #1e1e1e;
        color: white;
    }

    button[kind="header"] {
        background-color: transparent !important;
        color: white !important;
    }

    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }

    .chat-message {
        display: flex;
        align-items: flex-start;
        margin: 10px 0;
    }

    .chat-message.user {
        justify-content: flex-end;
        text-align: right;
        margin-right: 10px;
    }

    .chat-message.ai {
        justify-content: flex-start;
        text-align: left;
        margin-left: 10px;
    }

    .message-bubble {
        max-width: 70%;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }

    .message-bubble.user {
        background-color: #f63366 !important;
        color: white !important;
        border: 1px solid #ff4b7d !important;
        border-radius: 16px 16px 0 16px !important;
        margin-left: auto;
        margin-right: 0;
    }

    .message-bubble.ai {
        background-color: #2e2e2e;
        color: #f1f1f1;
        border: 1px solid #444;
        border-radius: 16px 16px 16px 0 !important;
        margin-right: auto;
    }

    .message-name {
        font-size: 12px;
        color: #aaa;
        margin-bottom: 3px;
    }

    textarea {
        background-color: #2b2b2b !important;
        color: white !important;
        border: 1px solid #444 !important;
    }

    label, .stTextArea label {
        color: white !important;
    }

    textarea::placeholder {
        color: #cccccc !important;
    }

    button[kind="primary"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 600;
        transition: background-color 0.3s ease;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
    }

    button[kind="primary"]:hover {
        background-color: #f63366 !important;
        color: #ffffff !important;
        border-color: #ff4b7d !important;
    }

    pre, code {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-radius: 8px;
        padding: 12px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 14px;
        overflow-x: auto;
    }

    pre::-webkit-scrollbar {
        height: 6px;
    }

    pre::-webkit-scrollbar-thumb {
        background: #444;
        border-radius: 4px;
    }

    button[title="Copy to clipboard"] {
        color: white !important;
        background-color: #1e1e1e !important;
        border: 1px solid #444 !important;
        border-radius: 6px !important;
    }

    button[title="Copy to clipboard"]:hover {
        background-color: #333 !important;
        color: white !important;
        border-color: #666 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Session Setup ----------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='font-size: 48px; margin: 0;'>❄️ NxT AI</h1>
    </div>
    """, unsafe_allow_html=True)

# ---------------- Chat Container ----------------
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        role = msg["role"]
        name = "Me" if role == "user" else "NxT AI"
        align = "user" if role == "user" else "ai"

        if isinstance(msg["content"], list):
            parts = []
            for item in msg["content"]:
                if item["type"] == "text":
                    parts.append(item["text"])
                elif item["type"] == "image_url":
                    parts.append(f"<img src='{item['image_url']['url']}' style='max-width: 100%; border-radius: 10px; margin-top: 8px;'>")
            content_html = "<br>".join(parts)
        else:
            content_html = msg["content"]

        st.markdown(f"""
            <div class="chat-message {align}">
                <div>
                    <div class="message-name">{name}</div>
                    <div class="message-bubble {align}">{content_html}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------- User Input ----------------
with st.form("user_input_form", clear_on_submit=True):
    user_input = st.text_area("Your message:", key="user_input", placeholder="Type your message here...", height=100)
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button("Send")

# ---------------- OpenRouter API ----------------
if submit_button and user_input:
    content_parts = [{"type": "text", "text": user_input}]

    if uploaded_file:
        base64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")
        content_parts.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
        })

    st.session_state["messages"].append({"role": "user", "content": content_parts})

    with chat_container:
        parts = []
        for part in content_parts:
            if part["type"] == "text":
                parts.append(part["text"])
            elif part["type"] == "image_url":
                parts.append(f"<img src='{part['image_url']['url']}' style='max-width: 100%; border-radius: 10px; margin-top: 8px;'>")
        content_html = "<br>".join(parts)

        st.markdown(f"""
            <div class="chat-message user">
                <div>
                    <div class="message-name">Me</div>
                    <div class="message-bubble user">{content_html}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Show typing...
        placeholder = st.empty()
        placeholder.markdown(
            """
            <div class="chat-message ai">
                <div>
                    <div class="message-name">NxT AI</div>
                    <div class="message-bubble ai">NxT AI is typing...</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "HTTP-Referer": "https://www.sitename.com",
                "X-Title": "SiteName",
                "Content-Type": "application/json",
            },
            json={
                "model": "google/gemini-2.5-pro-exp-03-25:free",
                "messages": st.session_state["messages"]
            },
        )
        data = response.json()
        bot_message = data["choices"][0]["message"]["content"]
    except Exception as e:
        bot_message = f"Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": bot_message})

    with chat_container:
        placeholder.markdown(
            f"""
            <div class="chat-message ai">
                <div>
                    <div class="message-name">NxT AI</div>
                    <div class="message-bubble ai">{bot_message}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
