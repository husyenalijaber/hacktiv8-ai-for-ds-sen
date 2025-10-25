import os
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

st.title("🤖 ChatBot-Ku (Google Gemini)")

def get_api_key_input():
    """Minta user untuk masukkan Google API Key."""
    if "GOOGLE_API_KEY" not in st.session_state:
        st.session_state["GOOGLE_API_KEY"] = ""

    if st.session_state["GOOGLE_API_KEY"]:
        return

    st.write("🔑 Masukkan Google API Key kamu:")

    col1, col2 = st.columns([4, 1])
    with col1:
        api_key = st.text_input(
            "Masukkan Google API Key",
            label_visibility="collapsed",
            type="password"
        )

    with col2:
        if st.button("Submit"):
            st.session_state["GOOGLE_API_KEY"] = api_key
            os.environ["GOOGLE_API_KEY"] = api_key
            st.rerun()

    if not st.session_state["GOOGLE_API_KEY"]:
        st.stop()


def load_llm():
    """Load LLM Gemini."""
    if "llm" not in st.session_state:
        st.session_state["llm"] = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    return st.session_state["llm"]


def get_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    return st.session_state["chat_history"]


def display_chat_message(message):
    role = "User" if isinstance(message, HumanMessage) else "AI"
    with st.chat_message(role):
        st.markdown(message.content)


def display_chat_history(chat_history):
    for chat in chat_history:
        display_chat_message(chat)


def user_query_to_llm(llm, chat_history):
    prompt = st.chat_input("💬 Tulis pesan kamu...")
    if not prompt:
        st.stop()

    chat_history.append(HumanMessage(content=prompt))
    display_chat_message(chat_history[-1])

    response = llm.invoke(chat_history)
    chat_history.append(response)
    display_chat_message(chat_history[-1])


def main():
    get_api_key_input()
    llm = load_llm()
    chat_history = get_chat_history()
    display_chat_history(chat_history)
    user_query_to_llm(llm, chat_history)


if __name__ == "__main__":
    main()
