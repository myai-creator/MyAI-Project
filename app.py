import streamlit as st
import requests

st.set_page_config(page_title="Всезнающий Ассистент Нова", page_icon="🤖", layout="centered")
st.title("🤖 Всезнающий Ассистент Нова")
st.write("Задайте абсолютно любой вопрос обо всем на свете, и Ассистент Нова подробно ответит вам!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я ваш всезнающий Ассистент Нова. Теперь я знаю весь интернет! О чем поговорим?"}
    ]

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
                # Надежный открытый шлюз к нейросетевой модели
                import urllib.parse
                encoded_text = urllib.parse.quote(user_query)
                url = f"https://pollinations.ai{encoded_text}"
                
                response = requests.get(url, timeout=25)
                if response.status_code == 200 and response.text:
                    ai_response = response.text
                else:
                    ai_response = "Сервер взял небольшую паузу. Пожалуйста, отправьте сообщение еще раз!"
            except Exception as e:
                ai_response = "Произошла сетевая заминка. Повторите попытку, пожалуйста."

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
