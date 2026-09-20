import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration constants
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "qwen/qwen3.8-27b"

# You could also add other configurations here, such as default values or timeouts.
