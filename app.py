import streamlit as st
import requests

st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="centered")
st.title("🤖 Мой ИИ Ассистент")
st.write("Задайте любой вопрос, и ИИ ответит вам, учитывая контекст беседы.")

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
                # Прямой и стабильный запрос к текстовой нейросети
                api_url = f"https://pollinations.ai{user_query}"
                response = requests.get(api_url, timeout=15)
                
                if response.status_code == 200:
                    ai_response = response.text
                else:
                    ai_response = "Сервер временно перегружен. Попробуйте еще раз!"
            except Exception as e:
                ai_response = "Не удалось подключиться. Проверьте интернет."

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
