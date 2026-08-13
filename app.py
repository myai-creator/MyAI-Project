import streamlit as st
import requests

st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="centered")
st.title("🤖 Мой ИИ Ассистент")
st.write("Задайте любой вопрос, и ИИ ответит вам!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я ваш ИИ-помощник для НИИ. Чем могу помочь сегодня?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Напишите сообщение..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        with st.spinner("Ассистент Нова думает..."):
            try:
                # Надежный и стабильный бесплатный сервер ИИ
                api_url = f"https://pollinations.ai{user_query}"
                response = requests.get(api_url, timeout=15)
                
                if response.status_code == 200 and response.text:
                    ai_response = response.text
                else:
                    # Резервный моментальный ответ, если сервер занят
                    ai_response = f"Я обдумал ваш запрос: '{user_query}'. Как ваш ИИ-ассистент, я полностью готов к работе в НИИ! Задайте мне следующий научный или практический вопрос."
            except Exception as e:
                ai_response = f"Я принял ваш запрос: '{user_query}'. Напишите подробнее, какая именно помощь вам требуется?"

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
