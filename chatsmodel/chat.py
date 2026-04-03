import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model

# 1. Load your .env from the parent folder (GenAi/)
load_dotenv(find_dotenv())

# 2. Initialize the model 
# Using a specific model ID like 'llama-3.3-70b-specdec' is best
model = init_chat_model(
    "qwen/qwen3-32b", 
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")
)

response = model.invoke("Who is zaryab Ahmad?")
print(response.content)