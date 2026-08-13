import streamlit as st

# 1. Настройка внешнего вида страницы
st.set_page_config(page_title="Ассистент Нова", page_icon="🤖")
st.title("🤖 Ассистент Нова")

# 2. Инициализация истории сообщений
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Отображение истории сообщений
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Поле ввода для пользователя (сюда можно писать абсолютно всё что угодно)
if user_query := st.chat_input("Напишите сообщение..."):
    # Выводим ваше сообщение на экран
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Спокойный и короткий ответ без подсказок и навязчивых предложений
    ai_response = f"Запрос '{user_query}' успешно принят в обработку и сохранен."

    # Выводим ответ на экран
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
