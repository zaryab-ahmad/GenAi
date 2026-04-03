import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate 
from langchain_groq import ChatGroq

# 1. Page Configuration
st.set_page_config(page_title="Movie Data Extractor", page_icon="🎬")
load_dotenv()

# 2. Initialize Model
model = ChatGroq(
    model="qwen/qwen3-32b", 
    api_key=os.getenv("GROQ_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)

# 3. Define Prompt Template
system_instruction = """
You are a highly accurate Data Extraction Engine. 
Convert the provided unstructured text into a JSON object.

REQUIRED JSON STRUCTURE:
{{
  "movie_title": "string",
  "year": integer or null,
  "director": "string or null",
  "genre": ["list", "of", "strings"],
  "lead_actors": ["list", "of", "top 3"],
  "box_office": "string or null",
  "one_sentence_synopsis": "string"
}}

Rules:
- If data is missing, use null.
- Output ONLY the JSON object.
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("human", "{unstructured_text}")
])

# 4. Streamlit UI
st.title("🎬 Movie Structured Data Extractor")
st.write("Paste a paragraph about a movie, and I'll turn it into structured JSON.")

# Input Area
raw_text = st.text_area("Unstructured Movie Text:", placeholder="e.g., In 1994, Frank Darabont directed The Shawshank Redemption...", height=200)

if st.button("Extract Data"):
    if not raw_text.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Analyzing text..."):
            try:
                # Chain Execution
                chain = prompt_template | model
                response = chain.invoke({"unstructured_text": raw_text})
                
                # Parse Result
                structured_data = json.loads(response.content)
                
                # Display Results
                st.success("Extraction Complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Data View")
                    st.write(f"**Title:** {structured_data.get('movie_title')}")
                    st.write(f"**Year:** {structured_data.get('year')}")
                    st.write(f"**Director:** {structured_data.get('director')}")
                    st.write(f"**Genres:** {', '.join(structured_data.get('genre', []))}")
                
                with col2:
                    st.subheader("JSON Output")
                    st.json(structured_data)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")