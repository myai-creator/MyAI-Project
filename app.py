import streamlit as st
import requests
import json

st.set_page_config(page_title="Всезнающий Ассистент Нова", page_icon="🤖", layout="centered")
st.title("🤖 Всезнающий Ассистент Нова")
st.write("Задайте абсолютно любой вопрос обо всем на свете, и нейросеть Google Gemini ответит вам!")

# ВАШ ЛИЧНЫЙ КЛЮЧ ИЗ GOOGLE AI STUDIO УЖЕ ВСТАВЛЕН СЮДА!
GOOGLE_API_KEY = "AQ.Ab8RN6LR3IrkzXfgvWiwYT-3iYQMzfN7cdJ_pP9bl5_zbSRwQw"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Привет! Я Ассистент Нова. Теперь я знаю весь интернет! Спросите меня о чем угодно, и я подробно отвечу."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Напишите сообщение..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        with st.spinner("Нова ищет ответ во всем интернете..."):
            try:
                # Отправляем запрос напрямую к официальному серверу Google Gemini с вашим ключом
                url = f"https://googleapis.com{GOOGLE_API_KEY}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts":[{"text": user_query + " (Отвечай строго на русском языке)"}]}]}
                
                response = requests.post(url, headers=headers, json=data, timeout=20)
                if response.status_code == 200:
                    ai_response = response.json()['candidates'][0]['content']['parts'][0]['text']
                else:
                    ai_response = "Сервер ИИ временно задумался. Пожалуйста, повторите ваш вопрос через секунду!"
            except Exception as e:
                ai_response = "Техническая заминка. Пожалуйста, отправьте сообщение повторно."

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
