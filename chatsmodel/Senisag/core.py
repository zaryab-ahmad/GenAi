import os
import json
from dotenv import load_dotenv
# FIX: Removed 'prompt_template' from the import list
from langchain_core.prompts import ChatPromptTemplate 
from langchain_groq import ChatGroq

load_dotenv()

# 1. Initialize the Groq Model
# Using JSON mode ensures the output is always a clean dictionary
model = ChatGroq(
    model="qwen/qwen3-32b", 
    api_key=os.getenv("GROQ_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}}
)

# 2. Define the Structured Extraction Prompt
# 2. Define the Structured Extraction Prompt
# Note the DOUBLE curly braces {{ }} around the JSON structure
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

# Keep this the same - single braces here are correct because it's a real variable
prompt = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("human", "{unstructured_text}")
])

# 3. Create the Chain
chain = prompt | model

# --- RUNNING THE EXTRACTION ---
raw_text = input("Enter unstructured text about a movie: ")

final_prompt = prompt.invoke({"unstructured_text": raw_text}
                             )

try:
    response = chain.invoke(final_prompt)
    
    # Parse the string content into a real Python Dictionary
    structured_data = json.loads(response.content)
    
    print("--- Successfully Extracted Data ---")
    print(json.dumps(structured_data, indent=4))

except Exception as e:
    print(f"An error occurred: {e}")