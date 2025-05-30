import streamlit as st
from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# --- Load env variables ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# --- Set Streamlit page config ---
st.set_page_config(page_title="🌐 Translator Agent", layout="centered")

# --- Custom CSS for dark theme, font, button styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, .stApp {
        background-color: #000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    .stTextArea textarea {
        background-color: #111 !important;
        color: #fff !important;
        border-radius: 8px;
        font-size: 20px;
        padding: 12px;
    }
            
      .stButton>button {
        background: linear-gradient(to right, #ff416c, #ff4b2b);
        color: white;
        border: none;
        padding: 0.6em 1.4em;
        border-radius: 30px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(to right, #2193b0, #6dd5ed);
    }

    .title {
        text-align: center;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 20px;
        color: #fff;
    }

    .desc {
        text-align: center;
        font-size: 16px;
        margin-bottom: 40px;
        color: #bbb;
    }

    .output-box {
        background-color: #111111;
        padding: 20px;
        border-radius: 10px;
        color: #e0e0e0;
        margin-top: 20px;
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title">🌍 Translator Agent</div>', unsafe_allow_html=True)

st.markdown('''
<div class="desc">
Sabreena 💖 helps your words shine in perfect English.<br>
🌟 Say it better, say it beautifully.
</div>
''', unsafe_allow_html=True)

# --- Input box ---
user_input = st.text_area("Enter text to translate:", placeholder="Ask a question", height=200)

# --- Async-safe wrapper for Runner ---
def run_sync_safe(agent, input, run_config):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(Runner.run(agent, input=input, run_config=run_config))

# --- Generate translation on button click ---
if st.button("Translate"):

    if not gemini_api_key:
        st.error("❌ GEMINI_API_KEY is not set. Please add it to your .env file.")
        st.stop()

    # --- Create Gemini client and model ---
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # --- Create Translator Agent ---
    translator_agent = Agent(
        name="Translator Agent",
        instructions="You are a translation agent. Translate the input to English.."
    )

    # --- Spinner while translating ---
    with st.spinner("Translating... please wait 🧠🌍"):
        result = run_sync_safe(
            translator_agent,
            input=user_input,
            run_config=config
        )

    # --- Output box with formatted text ---
        st.markdown('<div class="output-box">' + result.final_output.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)
        # repalce => Simple and quick