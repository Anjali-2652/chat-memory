# app.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("❌ Missing GOOGLE_API_KEY in .env")
    st.stop()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",  
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True,
    max_output_tokens=1024,
)

# explanation: 
# model → which Gemini model to use
# temperature (0.7) → creativity level
        # Low = more factual
        # High = more creative

# convert_system_message_to_human:
        # Gemini doesn’t natively support system messages
        # This converts system messages into human format
# max_output_tokens → maximum length of AI response


# Session state setup

if "chats" not in st.session_state:
    st.session_state.chats = {}  # {title: list of messages}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Ensure at least one chat exists
if not st.session_state.chats:
    st.session_state.chats["New Chat"] = []

# Sidebar: Manage Chats & Show History
with st.sidebar:
    st.header("💬 Chat Sessions")

    # Create new chat
    new_chat_title = st.text_input("New Chat Title", value="")
    if st.button("➕ Start New Chat") and new_chat_title.strip():
        title = new_chat_title.strip()
        if title not in st.session_state.chats:
            st.session_state.chats[title] = []
            st.session_state.current_chat = title
            st.rerun()
        else:
            st.warning(f"⚠️ '{title}' already exists.")

    # Select existing chat
    chat_titles = list(st.session_state.chats.keys())
    if chat_titles:
        try:
            idx = chat_titles.index(st.session_state.current_chat)
        except ValueError:
            idx = 0
        selected = st.selectbox("Switch Chat", chat_titles, index=idx)
        if selected != st.session_state.current_chat:
            st.session_state.current_chat = selected
            st.rerun()

    # Clear current chat
    if st.button("🗑️ Clear Current Chat"):
        st.session_state.chats[st.session_state.current_chat] = []
        st.rerun()

    st.divider()

    # 📜 Chat History Preview (like this interface!)
    current_msgs = st.session_state.chats.get(st.session_state.current_chat, [])

#     What this does:
        # Looks inside st.session_state.chats
        # Fetches messages for the currently selected chat
        # If the chat does not exist, it returns an empty list
    

    if current_msgs:
        with st.expander("📜 Chat History", expanded=False):
            # Show last 10 messages (most recent at bottom)
            for i, msg in enumerate(current_msgs[-10:]):
                role = "👤" if isinstance(msg, HumanMessage) else "🤖" # detect who send the message (human or ai)
                content = msg.content.strip()
                # Truncate long messages
                preview = (content[:47] + "...") if len(content) > 50 else content
                
                # Why truncate?
                    # Sidebar is small
                    # Long messages would look messy
                    # What this does:
                        # If message > 50 characters
                        # Show only first 47 characters + ...


                # Use subtle markdown styling
                st.caption(f"{role} {preview}")
    else:
        st.info("🗨️ Start chatting to see history here.")

    st.divider()
    st.caption("Chats persist across reloads. Create new topics anytime!")

# Get current chat (It fetches all messages of the currently selected chat from memory, and if nothing is found, it returns an empty list.)
current_messages = st.session_state.chats.get(st.session_state.current_chat, [])

# Main header
st.title(f"💬 {st.session_state.current_chat}")
st.caption("Powered by LangChain + Google Gemini")

# Display full chat in main area
for msg in current_messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.write(msg.content)

# User input
if prompt_input := st.chat_input("Ask me anything..."):
    # Add user message
    user_msg = HumanMessage(content=prompt_input)
    current_messages.append(user_msg)

    with st.chat_message("user", avatar="👤"):
        st.write(prompt_input)

    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful, friendly AI assistant named Gemi."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ])

            chain = prompt | llm
            response = chain.invoke({
                "input": prompt_input,
                "chat_history": current_messages[:-1]
            })

        st.write(response.content)
        current_messages.append(AIMessage(content=response.content))

    # Save & refresh
    st.session_state.chats[st.session_state.current_chat] = current_messages
    st.rerun()