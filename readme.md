
# 💬 Streamlit Chat App with Google Gemini (LangChain)

A **multi-session AI chat application** built using **Streamlit**, **LangChain**, and **Google Gemini**.  
The app supports multiple chat threads, sidebar chat history previews, and context-aware conversations—similar to the ChatGPT interface.

## 🧠 How It Works

1. **Streamlit** provides the web interface and handles UI reruns.
2. **Session State** stores chat sessions and message history.
3. **LangChain** structures prompts and manages chat messages.
4. **Google Gemini** generates intelligent responses.
5. Previous messages are sent back to the model to maintain context.

### create virtual environment, make sure install python 10 because in the latest version,  langchain in not support good
py -3.10 -m venv venv

### Activate
venv\scripts\activate

### installation 
pip install -r requirements.txt


### Create .env files 
GOOGLE_API_KEY=Your-gemini-api-key

### to run

streamlit run app.py



