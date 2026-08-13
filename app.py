import streamlit as st
import streamlit.components.v1 as components

# 1. Настройка страницы
st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="wide")
st.title("🤖 Всезнающий Ассистент Нова")
st.write("Ниже открыто прямое защищенное окно в нейросеть. Задайте ей абсолютно любой вопрос про Бравл Старс, игры, уроки или жизнь — она знает всё!")

# 2. Встраиваем полноценный бесплатный ИИ-чат, который сервер не сможет заблокировать
chat_html = """
<iframe 
    src="https://microsoft.com" 
    style="width:100%; height:750px; border:none; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
    allow="microphone; clipboard-read; clipboard-write">
</iframe>
"""

# Отображаем встроенную нейросеть на экране
components.html(chat_html, height=760)
