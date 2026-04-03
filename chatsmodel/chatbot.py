import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 1. Load your .env
load_dotenv(find_dotenv())

# 2. Initialize the model with a CURRENT model ID
model = init_chat_model(
    "qwen/qwen3-32b",  # FIXED: Using the active 2026 model ID
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")
)

# Initialize history with your System instruction
messages = [
    SystemMessage(content="You are a funny AI agent who cracks jokes.")
]

while True:
    prompt = input("\nEnter your prompt (or 'quit' to exit): ")
    if prompt.lower() == "quit":
        break
    
    # Add user message to history
    messages.append(HumanMessage(content=prompt))

    try:
        # Pass the ENTIRE list to the model
        response = model.invoke(messages)
        
        # Add AI response to history
        messages.append(response)
        
        print(f"\nAI: {response.content}")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Tip: Check your Groq console for the latest active model IDs.")