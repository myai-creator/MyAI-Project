import streamlit as st
import streamlit.components.v1 as components

# 1. Настройка страницы
st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="wide")
st.title("🤖 Всезнающий Ассистент Нова")
st.write("Ниже открыто полноценное, бесплатное и всезнающее окно ИИ. Задайте абсолютно любой вопрос — эта нейросеть знает всё на свете!")

# 2. Встраиваем безотказный и бесплатный ИИ-чат DuckDuckGo
chat_html = """
<iframe 
    src="https://duckduckgo.com" 
    style="width:100%; height:750px; border:none; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
    allow="microphone; clipboard-read; clipboard-write">
</iframe>
"""

# Отображаем встроенную нейросеть на экране
components.html(chat_html, height=760)
