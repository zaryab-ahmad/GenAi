import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

st.set_page_config(page_title="GenAi Bot", page_icon="🤖")
st.title("🤖 My GenAI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant").write(msg.content)

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)
    
    model = ChatGroq(model="qwen/qwen3-32b", api_key=os.getenv("GROQ_API_KEY"))
    response = model.invoke(st.session_state.messages)
    
    st.session_state.messages.append(response)
    st.chat_message("assistant").write(response.content)