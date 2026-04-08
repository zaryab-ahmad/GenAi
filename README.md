# 🎬 GenAI Movie Data Extractor 

This project is a **Structured Information Extraction** tool built following the [Sheryians AI School](https://www.youtube.com/@SheryiansAISchool) Generative AI series. It uses Large Language Models to transform messy movie descriptions into clean, machine-readable JSON.

## 🌟 Features
- **Zero-Shot Extraction:** Uses `Qwen-32B` (via Groq) to understand context without specific training.
- **Structured Output:** Forced JSON formatting for seamless data integration.
- **Interactive UI:** A clean **Streamlit** dashboard to test extractions in real-time.
- **LangChain Integration:** Uses LCEL (LangChain Expression Language) for a modular pipeline.

## 🛠️ Tech Stack
- **LLM:** Qwen 3 (Inference via **Groq Cloud**)
- **Orchestration:** **LangChain**
- **Frontend:** **Streamlit**
- **Language:** Python 3.10+

## 📂 Project Structure
- `chatsmodel/`: Contains the core logic and Streamlit UI.
- `.env`: Stores sensitive API keys (Excluded from GitHub).
- `requirements.txt`: Managed dependencies for easy setup.

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/zaryab-ahmad/GenAi.git](https://github.com/zaryab-ahmad/GenAi.git)
cd GenAi

2. Setup Virtual Environment
Bash
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate 
3. Install Requirements
Bash
pip install -r requirements.txt
4. API Configuration
Create a .env file in the root directory and add your key:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
5. Run the App
Bash
streamlit run chatsmodel/Senisag/movie_app.py
📊 Example Result
Input Text:

"Christopher Nolan's 2010 masterpiece Inception starring Leonardo DiCaprio is a mind-bending sci-fi heist film. It earned over $836 million at the box office."

Extracted JSON:

JSON
{
  "movie_title": "Inception",
  "year": 2010,
  "director": "Christopher Nolan",
  "genre": ["Sci-Fi", "Action"],
  "lead_actors": ["Leonardo DiCaprio"],
  "box_office": "$836 million"
}
🤝 Acknowledgments
Huge shoutout to Akash Vyas for the #GenAIStarts series on Sheryians AI School!


---

### 🚀 Final Push Instructions:
1. Open your `README.md` file in VS Code.
2. Delete any old text and **paste** the block above.
3. Save the file.
4. Run these three commands in your terminal to finish:

```cmd
git add README.md
git commit -m "docs: finalize project readme"
git push