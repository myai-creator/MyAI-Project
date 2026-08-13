import streamlit as st
import time

# 1. Настройка внешнего вида страницы
st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="centered")
st.title("🤖 Мой ИИ Ассистент")
st.write("Задайте любой вопрос, и ИИ ответит вам, учитывая контекст беседы.")

# 2. Инициализация истории сообщений в памяти сессии (чтобы чат не стирался при обновлении)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я ваш ИИ-помощник для НИИ. Чем могу помочь сегодня?"}
    ]

# 3. Отображение всех предыдущих сообщений из истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Поле ввода для пользователя (всегда закреплено внизу экрана)
if user_query := st.chat_input("Напишите сообщение..."):
    
    # Отображаем сообщение пользователя в чате
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Добавляем его в историю памяти
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Отображаем блок ответа ИИ
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Шаблон заглушки ответа (в будущем здесь будет реальный запрос к API нейросети)
        fake_response = f"Вы написали: «{user_query}». Я принял этот запрос в обработку для нашего НИИ. Система хранения контекста работает, я помню всю нашу переписку!"
        
        # Эффект печатающегося текста (Streaming)
        for chunk in fake_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.08)  # Скорость появления слов
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
        
    # Добавляем ответ ИИ в историю памяти
    st.session_state.messages.append({"role": "assistant", "content": full_response})