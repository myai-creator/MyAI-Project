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
                # Используем стабильную открытую модель Qwen через бесплатный API Hugging Face
                API_URL = "https://huggingface.co"
                payload = {
                    "inputs": user_query,
                    "parameters": {"max_new_tokens": 500, "return_full_text": False}
                }
                response = requests.post(API_URL, json=payload, timeout=20)
                
                if response.status_code == 200:
                    res_json = response.json()
                    # Проверяем формат ответа
                    if isinstance(res_json, list) and "generated_text" in res_json[0]:
                        ai_response = res_json[0]["generated_text"]
                    elif isinstance(res_json, dict) and "generated_text" in res_json:
                        ai_response = res_json["generated_text"]
                    else:
                        ai_response = str(res_json)
                else:
                    # Если модель загружается в память сервера, она просит подождать пару секунд
                    ai_response = "ИИ просыпается и загружает базу данных. Пожалуйста, повторите этот вопрос еще раз через 5 секунд!"
            except Exception as e:
                ai_response = "Произошел технический сбой при связи с сервером. Попробуйте еще раз."

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
