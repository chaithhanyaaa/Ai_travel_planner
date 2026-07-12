import os

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# -----------------------
# Ollama Configuration
# -----------------------
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))

# -----------------------
# Tavily Configuration
# -----------------------
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

TAVILY_MAX_RESULTS = int(os.getenv("TAVILY_MAX_RESULTS", "5"))

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing. Please add it to your .env file."
    )

ORS_API_KEY = os.getenv("ORS_API_KEY")

if not ORS_API_KEY:
    raise ValueError(
        "ORS_API_KEY is missing. Please add it to your .env file."
    )