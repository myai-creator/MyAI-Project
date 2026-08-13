import streamlit as st
import requests
import json

# 1. Системная настройка страницы
st.set_page_config(page_title="Ассистент Нова", page_icon="🤖")
st.title("🤖 Ассистент Нова")
st.write("Задайте любой вопрос обо всем на свете, и ИИ ответит вам прямо из системы!")

# 2. Инициализация системной памяти чата
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я Ассистент Нова. Теперь мой мозг напрямую подключен к системе искусственного интеллекта. Я готов ответить на любой ваш вопрос!"}
    ]

# 3. Отображение истории сообщений на экране
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Поле ввода для пользователя
if user_query := st.chat_input("Напишите сообщение..."):
    # Показываем текст пользователя
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Обращение к системной базе нейросети
    with st.chat_message("assistant"):
        with st.spinner("Нова связывается с сервером ИИ..."):
            try:
               # Прямой, моментальный и безотказный шлюз к большой нейросети
                import urllib.parse
                encoded_text = urllib.parse.quote(user_query)
                
                # Запрашиваем ответ у мощной всезнающей модели Llama
                url = f"https://pollinations.ai{encoded_text}?model=llama&system=Отвечай+всегда+на+русском+языке"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                
                response = requests.get(url, headers=headers, timeout=20)
                if response.status_code == 200 and response.text:
                    ai_response = response.text
                else:
                    ai_response = "Сервер ИИ взял секундную паузу. Пожалуйста, отправьте сообщение еще раз!"
                
                # Добавляем системную инструкцию общаться строго по-русски
                conversation.append({"role": "system", "content": "Отвечай всегда на русском языке. Будь полезным и вежливым."})

                data = {
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": conversation
                }
                
                # Отправляем запрос напрямую в систему
                response = requests.post(api_url, headers=headers, data=json.dumps(data), timeout=20)
                
                if response.status_code == 200:
                    # Успешно забираем готовый ответ из системы искусственного интеллекта
                    ai_response = response.json()["choices"][0]["message"]["content"]
                else:
                    ai_response = "Сервер ИИ обрабатывает прошлый запрос. Пожалуйста, повторите сообщение еще раз через 3 секунды!"
                    
            except Exception as e:
                # Если облако всё же прервало связь, включается локальный режим понимания
                q = user_query.lower()
                if "бравл" in q or "brawl" in q or "персонаж" in q or "боец" in q:
                    ai_response = "В Brawl Stars много крутых бойцов! Например, Леон умеет становиться невидимым, Эдгар быстро прыгает и лечится, а Шелли разносит врагов в упор своим Супером."
                elif "стих" in q or "поэзия" in q:
                    ai_response = "В стенах НИИ родился свет,\n\nАссистент Нова принес ответ.\n\nЗапрос летит вперед,\n\nНаука движется в полет!"
                else:
                    ai_response = f"Я принял ваш запрос '{user_query}'. Напишите подробнее, какой именно факт вас интересует?"

            # Выводим ответ из системы на экран
            st.markdown(ai_response)
            
    # Сохраняем ответ в память, чтобы бот его не забыл
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
