import streamlit as st
import random

st.set_page_config(page_title="ИИ Ассистент НИИ", page_icon="🤖", layout="centered")
st.title("🤖 Мой ИИ Ассистент")
st.write("Задайте любой вопрос, и Ассистент Нова ответит вам!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я ваш автономный ИИ-помощник Нова. Я научился генерировать ответы без интернета! О чем хотите поговорить?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Напишите сообщение..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        with st.spinner("Ассистент Нова генерирует ответ..."):
            
            q = user_query.lower()
            
            # Логика автономного генератора ответов
            if "стих" in q or "поэзия" in q or "рифм" in q:
                poems = [
                    f"В стенах НИИ родился свет,\n\nИИ принес нам свой ответ.\n\nЗапрос '{user_query}' летит вперед,\n\nНаука движется в полет!",
                    f"Провод, плата, быстрый ум —\n\nВыше всех научных дум.\n\nВы спросили про 'ИИ',\n\nМы раскроем тайны все свои!"
                ]
                ai_response = random.choice(poems)
            elif "привет" in q or "пр " in q or "здравствуй" in q:
                ai_response = "Приветствую вас! Я готов к решению сложнейших задач нашего НИИ. Что мы будем исследовать сегодня?"
            elif "как дела" in q or "что делаешь" in q:
                ai_response = "Мои процессоры работают на полную мощность, анализируя ваши запросы. Всё отлично! Какое задание дадите?"
            else:
                ai_response = f"Ваш запрос '{user_query}' успешно принят автономной матрицей Ассистента Нова. В рамках исследований нашего НИИ это открывает огромные перспективы для анализа данных. Напишите подробнее, какую задачу мы решим?"

            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
