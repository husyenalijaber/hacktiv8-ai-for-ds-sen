# app-02.py
import os
import streamlit as st
import replicate

st.set_page_config(page_title="ChatBot IBM Granite")
st.title("🤖 ChatBot IBM Granite (via Replicate)")

MODEL_ID = "ibm-granite/granite-3.1-8b-instruct"

# ===== Input API Token =====
if "REPLICATE_API_TOKEN" not in st.session_state:
    st.session_state["REPLICATE_API_TOKEN"] = ""

if not st.session_state["REPLICATE_API_TOKEN"]:
    st.write("Masukkan Replicate API Token (dapatkan dari https://replicate.com/account/api-tokens)")
    col1, col2 = st.columns((80, 20))
    with col1:
        api_token = st.text_input("", type="password", label_visibility="collapsed")
    with col2:
        if st.button("Submit"):
            st.session_state["REPLICATE_API_TOKEN"] = api_token.strip()
            os.environ["REPLICATE_API_TOKEN"] = api_token.strip()
            st.rerun()

if not st.session_state["REPLICATE_API_TOKEN"]:
    st.stop()

# ===== Chat History =====
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def display_chat():
    for role, text in st.session_state["chat_history"]:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(text)

display_chat()

# ===== Chat Input =====
prompt = st.chat_input("Ketik pesan untuk Granite...")
if prompt:
    # Tampilkan pesan user
    st.session_state["chat_history"].append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Panggil API Replicate
    try:
        with st.chat_message("assistant"):
            with st.spinner("IBM Granite sedang berpikir..."):
                output = replicate.run(MODEL_ID, input={"prompt": prompt})
                if isinstance(output, list):
                    response = "".join(output)
                else:
                    response = str(output)
                st.markdown(response)
    except Exception as e:
        response = f"[Error] {e}"
        st.error(response)

    # Simpan ke history
    st.session_state["chat_history"].append(("assistant", response))
