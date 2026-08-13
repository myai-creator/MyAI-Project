import streamlit as st
import requests
import json

# 1. Настройка внешнего вида страницы
st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="centered")
st.title("🤖 Мой ИИ Ассистент")
st.write("Задайте любой вопрос, и ИИ ответит вам, учитывая контекст беседы.")

# 2. Инициализация истории сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я ваш ИИ-помощник для НИИ. Чем могу помочь сегодня?"}
    ]

# 3. Отображение всех предыдущих сообщений из истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Поле ввода для пользователя
if user_query := st.chat_input("Напишите сообщение..."):
    # Отображаем сообщение пользователя в чате
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Добавляем в память сессии
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Формируем ответ искусственного интеллекта
    with st.chat_message("assistant"):
        with st.spinner("Ассистент Нова думает..."):
            try:
                # Отправляем запрос к бесплатной нейросети через открытый API-интерфейс
                api_url = "https://openrouter.ai"
                headers = {"Content-Type": "application/json"}
                data = {
                    "model": "google/gemini-2.5-flash",
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                }
                response = requests.post(api_url, headers=headers, data=json.dumps(data), timeout=15)
                
                if response.status_code == 200:
                    ai_response = response.json()["choices"][0]["message"]["content"]
                else:
                    ai_response = "Система приняла запрос, но сервер временно перегружен. Попробуйте еще раз!"
            except Exception as e:
                ai_response = "Не удалось подключиться к нейросети. Проверьте интернет на устройстве."

            st.markdown(ai_response)
            
    # Добавляем ответ ИИ в память сессии
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
