import streamlit as st
import requests
import urllib.parse

# 1. Настройка внешнего вида страницы
st.set_page_config(page_title="ИИ Ассистент Нова", page_icon="🤖", layout="centered")
st.title("🤖 Всезнающий Ассистент Нова")
st.write("Задайте любой вопрос обо всем на свете (например, про Brawl Stars), и ИИ ответит вам!")

# 2. Инициализация истории сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я Ассистент Нова. Теперь я знаю всё на свете и готов ответить на любой ваш вопрос. О чем поговорим?"}
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

    # Запрос к нейросети
    with st.chat_message("assistant"):
        with st.spinner("Нова думает..."):
            try:
                # Безопасно кодируем текст вопроса, чтобы не ломать ссылку пробелами
                encoded_query = urllib.parse.quote(user_query)
                
                # Используем стабильный текстовый сервер с инструкцией отвечать по-русски
                url = f"https://pollinations.ai{encoded_query}?system=Отвечай+всегда+на+русском+языке"
                
                # Добавляем браузерный заголовок, чтобы облако Streamlit не блокировало запрос
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200 and response.text:
                    ai_response = response.text
                else:
                    ai_response = "Извините, сервер временно перегружен. Попробуйте отправить сообщение еще раз!"
            except Exception as e:
                ai_response = "Не удалось подключиться к серверу нейросети. Пожалуйста, повторите попытку."

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
