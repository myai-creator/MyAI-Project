import streamlit as st
import requests
import urllib.parse

# 1. Системные настройки страницы
st.set_page_config(page_title="Ассистент Нова", page_icon="🤖")
st.title("🤖 Всезнающий Ассистент Нова")
st.write("Приложение подключено к глобальной системе ИИ. Задайте любой вопрос обо всем на свете!")

# 2. Инициализация памяти чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Вывод истории сообщений
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Поле ввода для пользователя (работает с любой темой)
if user_query := st.chat_input("Напишите абсолютно любой вопрос..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        with st.spinner("Нова ищет ответ в глобальной сети ИИ..."):
            try:
                # Безопасное кодирование текста для передачи по сети
                safe_text = urllib.parse.quote(user_query)
                
                # Запрос к открытому всезнающему ядру ИИ (модель Llama)
                api_url = f"https://pollinations.ai{safe_text}?model=llama&system=Отвечай+всегда+на+русском+языке"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                
                response = requests.get(api_url, headers=headers, timeout=25)
                
                if response.status_code == 200 and response.text:
                    ai_response = response.text
                else:
                    ai_response = "Сервер глобального ИИ перегружен. Пожалуйста, отправьте сообщение еще раз!"
            except Exception as e:
                ai_response = "Не удалось связаться с сетью ИИ. Проверьте подключение интернета на ноутбуке."

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
