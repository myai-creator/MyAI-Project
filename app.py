import streamlit as st
import requests

# 1. Настройка внешнего вида страницы
st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="centered")
st.title("🤖 Мой ИИ Ассистент")
st.write("Задайте абсолютно любой вопрос, и Ассистент Нова ответит вам!")

# 2. Инициализация истории сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я ваш всезнающий ИИ-помощник Нова. Теперь я подключен к большой нейросети и могу ответить абсолютно на любой ваш вопрос! О чем поговорим?"}
    ]

# 3. Отображение истории сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Поле ввода для пользователя
if user_query := st.chat_input("Напишите сообщение..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Запрос к настоящей нейросети
    with st.chat_message("assistant"):
        with st.spinner("Ассистент Нова думает..."):
            try:
                # Отправляем запрос к открытому и бесплатному серверу текстовой нейросети
                import urllib.parse
                safe_query = urllib.parse.quote(user_query)
                api_url = f"https://pollinations.ai{safe_query}"
                
                # Добавляем заголовки, чтобы сервер Streamlit не блокировал соединение
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = requests.get(api_url, headers=headers, timeout=20)
                
                if response.status_code == 200 and response.text:
                    ai_response = response.text
                else:
                    ai_response = "Сервер ИИ сейчас немного занят, пожалуйста, повторите ваш вопрос еще раз!"
            except Exception as e:
                ai_response = "Произошла заминка при подключении к сети. Попробуйте отправить сообщение повторно."

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
