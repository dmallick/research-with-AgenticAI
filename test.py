
import os
import getpass

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(OPENAI_API_KEY)

# moonshotai/Kimi-K2-Thinking
MODEL_ID = "moonshotai/Kimi-K2-Thinking"
PROVIDER = "auto"
