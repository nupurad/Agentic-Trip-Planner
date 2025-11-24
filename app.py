import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"  # Backend endpoint


st.set_page_config(
    page_title="WanderBot",
    page_icon="🌍",
    layout="wide",
)

st.markdown("""
    <style>
        /* Main Page Background */
        .main {
            background-color: #0B1E34; /* Deep Navy */
        }

        /* Chat Containers */
        .chat-container {
            padding: 1.2rem;
            border-radius: 14px;
            background-color: rgba(255,255,255,0.04);
            backdrop-filter: blur(6px);
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25);
            margin-bottom: 1rem;
        }

        /* User Message Bubble */
        .user-msg {
            background-color: #C9E4FF;  /* Light Blue */
            padding: 0.9rem;
            border-radius: 12px;
            margin-bottom: 10px;
            font-size: 1.1rem;
            color: #0B1E34;  /* Navy text */
        }

        /* Bot Message Bubble */
        .bot-msg {
            background-color: #D1F2EB;  /* Soft Teal */
            padding: 0.9rem;
            border-radius: 12px;
            margin-bottom: 10px;
            font-size: 1.1rem;
            color: #0B1E34; /* Navy text */
        }

        /* Title Gradient */
        .title-text {
            font-size: 2.8rem !important;
            font-weight: 800;
            background: linear-gradient(90deg, #3BC9DB, #228BE6); /* Aqua → Blue */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: -4px;
        }

        .subtitle-text {
            font-size: 1.25rem !important;
            color: #A8CBEF; /* Soft Blue */
            text-align: center;
            margin-bottom: 30px;
        }

        .footer-note {
            text-align:center;
            color: #B8C8D4;
            margin-top: 40px;
            font-size: 0.85rem;
        }

        /* Input Box */
        .stTextInput>div>div>input {
            background-color: #11263F; /* Navy input */
            color: #E3F2FD;
            border-radius: 10px;
            border: 1px solid #3BC9DB;
        }

        /* Button */
        .stButton>button {
            background: linear-gradient(90deg, #3BC9DB, #228BE6);
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            font-size: 1.1rem;
            border: none;
        }

        .stButton>button:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    :root {
        --footer-height: 64px; /* change if you want a taller/shorter footer */
    }

    /* ensure full viewport height */
    .main {
        min-height: 100vh;
        position: relative;
    }

    /* give the page content bottom padding so it never sits under the fixed footer */
    .block-container {
        padding-bottom: calc(var(--footer-height) + 24px); /* extra breathing room */
    }

    /* style the footer and fix it to bottom */
    .footer-note {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        height: var(--footer-height);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        /* visual styles — tweak to match your theme */
        backdrop-filter: blur(6px);
        color: #B8C8D4;
        font-size: 0.9rem;
        box-shadow: 0 -6px 18px rgba(2,10,20,0.4);
    }

    /* small-screen tweak: reduce footer height */
    @media (max-width: 600px) {
        :root { --footer-height: 56px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown("<div class='title-text'>WanderBot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Your AI-powered trip planner using LangGraph + FastAPI ✈️</div>", unsafe_allow_html=True)

st.write("")

if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("### Let's plan you an amazing trip!")

chat_box = st.container()

with chat_box:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            st.markdown(
                f"<div class='chat-container user-msg'><strong>You:</strong> {content}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-container bot-msg'><strong>AI Agent:</strong> {content}</div>",
                unsafe_allow_html=True,
            )


st.write("---")
st.markdown("### 🌄 Where to, next?")

user_input = st.text_input("", placeholder="e.g. Plan a 7-day Australia trip")

if st.button("Generate Plan"):
    if user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Creating your itinerary..."):
            try:
                payload = {"question": user_input}
                response = requests.post(f"{BASE_URL}/query", json=payload)

                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")

                    formatted_answer = (
                        f"🌍 Your Travel Plan ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})\n"
                        f"{answer}\n\n"
                        "*⚠️ Responses are generated by AI. Please verify prices, timings, and travel regulations.*"
                    )

                    st.session_state.messages.append({"role": "assistant", "content": formatted_answer})
                else:
                    st.error("❌ Bot failed to respond: " + response.text)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

        st.rerun()

st.markdown("<div class='footer-note'>Built with ❤️ using LangGraph, FastAPI & Streamlit</div>", unsafe_allow_html=True)

