import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate 
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

# Load environment variables
load_dotenv()

# --- 1. DATA MODEL ---
class Movie(BaseModel):
    movie_title: str = Field(description="The full title of the movie")
    year: Optional[int] = Field(description="The release year of the movie")
    director: Optional[str] = Field(description="The name of the director")
    genre: List[str] = Field(default_factory=list, description="List of movie genres")
    lead_actors: List[str] = Field(default_factory=list, description="List of main cast members")
    box_office: Optional[str] = Field(description="Financial earnings of the movie")
    one_sentence_synopsis: str = Field(description="A brief summary of the plot")

parser = PydanticOutputParser(pydantic_object=Movie)

# --- 2. STREAMLIT UI CONFIG ---
st.set_page_config(page_title="Movie Data Extractor", page_icon="🎬", layout="wide")

st.title("🎬 Movie Structured Data Extractor")
st.markdown("""
Transform unstructured movie reviews or descriptions into clean, organized data using **LangChain** and **Groq AI**.
""")

# --- 3. SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Groq API Key", type="password")
    
    st.info("This app uses the **Qwen-32B** model for high-speed extraction.")

# --- 4. MAIN INTERFACE ---
if api_key:
    # Initialize the Model
    model = ChatGroq(
        model="llama-3.3-70b-versatile", 
        api_key=api_key,
        model_kwargs={"response_format": {"type": "json_object"}}
    )

    # Define the Prompt
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a data extraction expert. Extract information precisely. \n{format_instructions}"),
        ("human", "{unstructured_text}")
    ])

    # Input Section
    st.subheader("📥 Input")
    raw_text = st.text_area(
        "Paste your movie paragraph here:", 
        height=200, 
        placeholder="Example: Christopher Nolan's 2014 space epic Interstellar starring Matthew McConaughey..."
    )

    if st.button("Extract Data 🚀"):
        if raw_text.strip():
            with st.spinner("🤖 AI is analyzing the text..."):
                try:
                    # Run the Chain
                    final_prompt = prompt_template.invoke({
                        "unstructured_text": raw_text,
                        "format_instructions": parser.get_format_instructions()
                    })
                    
                    response = model.invoke(final_prompt)
                    structured_data = json.loads(response.content)

                    # --- 5. DISPLAY RESULTS ---
                    st.success("Extraction Complete!")
                    st.divider()

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.subheader("📋 Core Information")
                        st.write(f"**🎥 Movie Title:** {structured_data.get('movie_title')}")
                        st.write(f"**📅 Year:** {structured_data.get('year')}")
                        st.write(f"**🎬 Director:** {structured_data.get('director')}")
                        st.write(f"**💰 Box Office:** {structured_data.get('box_office')}")
                        
                        st.subheader("📝 Synopsis")
                        st.info(structured_data.get('one_sentence_synopsis'))

                    with col2:
                        st.subheader("🎭 Cast & Style")
                        st.write("**Actors:**")
                        for actor in structured_data.get('lead_actors', []):
                            st.write(f"- {actor}")
                        
                        st.write("**Genres:**")
                        for g in structured_data.get('genre', []):
                            st.badge(g)

                    with st.expander("🔍 View Raw JSON Output"):
                        st.json(structured_data)

                except Exception as e:
                    st.error(f"Failed to extract data. Error: {e}")
        else:
            st.warning("Please enter some text before clicking extract.")
else:
    st.warning("⚠️ Please provide a Groq API Key in your .env file or the sidebar to continue.")