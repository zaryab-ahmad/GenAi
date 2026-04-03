from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# 1. Specify the model ID (0.5B is ~900MB - perfect for your first local test)
model_id = "Qwen/Qwen2.5-0.5B"

print(f"--- Loading {model_id} to your local machine ---")
print("Note: This may take a few minutes the first time while it downloads...")

# 2. Use native Transformers to load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# 3. Create the pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=100,
    temperature=0.7,
    device=-1 # Use -1 for CPU, or 0 if you have an NVIDIA GPU
)

# 4. Wrap it for LangChain
llm = HuggingFacePipeline(pipeline=pipe)
chat_model = ChatHuggingFace(llm=llm)

# 5. Run the query
print("\n--- Generating Response ---")
response = chat_model.invoke("What is the capital of France?")
print(f"\nAI Response: {response.content}")