import os
import chainlit as cl
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

# 1. Setup the Model
model = ChatGroq(
    model="qwen/qwen3-32b", 
    api_key=os.getenv("GROQ_API_KEY"),
    streaming=True # Crucial for that "typing" effect
)

@cl.on_chat_start
async def start():
    # Initialize session history with a System Message
    cl.user_session.set("messages", [
        SystemMessage(content="You are a funny AI agent built with Chainlit.")
    ])
    await cl.Message(content="Hello! I am your funny AI. How can I help you?").send()

@cl.on_message
async def main(message: cl.Message):
    # Retrieve history from session
    messages = cl.user_session.get("messages")
    
    # Add user message
    messages.append(HumanMessage(content=message.content))
    
    # Prepare the UI message to stream into
    msg = cl.Message(content="")
    
    # 2. Stream the response
    async for chunk in model.astream(messages):
        if chunk.content:
            await msg.stream_token(chunk.content)
    
    # Save the full AI response to history
    messages.append(AIMessage(content=msg.content))
    await msg.send()