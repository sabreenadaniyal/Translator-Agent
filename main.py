from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

# --- Load env variables ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# --- Check if the API key is present; if not, raise an error ---
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Get user input from terminal
user_input = input("Enter text to translate: ")

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
    instructions="You are a translation agent .only Translate the input to English.."
)

# --- translating ---
response = Runner.run_sync(
    translator_agent,
    input = user_input,
    run_config = config
)
print("💬Translated Output:")
print(response.final_output)