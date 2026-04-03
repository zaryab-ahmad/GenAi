import os
import importlib
from dotenv import load_dotenv, find_dotenv

# 1. Safety Check: Verify the library is actually installed in this .venv
try:
    importlib.import_module('sentence_transformers')
    print("✅ sentence-transformers is detected.")
except ImportError:
    print("❌ ERROR: sentence-transformers is still missing from this environment.")
    print("Run: pip install sentence-transformers")

# 2. Load environment
load_dotenv(find_dotenv())

# 3. Import LangChain bits
from langchain_huggingface import HuggingFaceEmbeddings

model_name = "SproutsAI/embedding-model"

print(f"--- Initializing {model_name} ---")

# 4. Initialize
embeddings_model = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={'trust_remote_code': True}
)

# 5. Test with your text
texts = ["Hello world", "How are you?"]

try:
    vector_data = embeddings_model.embed_documents(texts)
    print(f"\n✅ Success! Generated {len(vector_data)} vectors.")
    print(f"Vector Dimensions: {len(vector_data[0])}")
    print(f"Snippet of first vector: {vector_data[0][:5]}...")
except Exception as e:
    print(f"❌ Error during embedding: {e}")