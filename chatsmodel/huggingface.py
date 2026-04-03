import os
from dotenv import load_dotenv, find_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

# 1. Try to find the .env file
dotenv_path = find_dotenv()
if not dotenv_path:
    print("❌ ERROR: Could not find your .env file! Make sure it is in C:\\Users\\zarya\\Desktop\\GenAi\\.env")
else:
    print(f"✅ Found .env at: {dotenv_path}")
    load_dotenv(dotenv_path)

# 2. Get the token and check it
token = os.getenv("HF_TOKEN")

if token is None:
    print("❌ ERROR: 'HF_TOKEN' was not found inside your .env file.")
    print("Please open your .env and make sure it has this line: HF_TOKEN=your_token_here")
else:
    # Set the variable LangChain expects
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = token
    print("✅ Token loaded successfully.")

    # 3. Setup the Endpoint
    try:
        llm = HuggingFaceEndpoint(
            repo_id="deepseek-ai/DeepSeek-R1",
            task="text-generation",
            huggingfacehub_api_token=token,
            timeout=300
        )

        model = ChatHuggingFace(llm=llm)

        print("--- Connecting to DeepSeek-R1 ---")
        response = model.invoke("Who are you?")
        print("\nDeepSeek Response:")
        print(response.content)

    except Exception as e:
        print(f"\n❌ AI Error: {e}")