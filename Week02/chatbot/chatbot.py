import streamlit as st

from open_ai_chat import chat


def main():
    st.set_page_config(page_title="YWS ChatBot", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title(":red[Y]:green[W]:blue[S] Chatbot")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "안녕! YWS 챗봇이야. 뭘 도와줄까?"  # 원하는 인사말을 입력합니다.
                                         }]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("질문을 입력해주세요."):
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(messages=generate_chat_prompt_with_history(st.session_state.chat_history, query))
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        add_message_to_history(st.session_state.chat_history, "assistant", response)

def create_user_chat_prompt(user_message):
    return f"""
            당신은 YWS 챗봇입니다.
            언제나 친절하게 답변하고, 사용자에게 행복을 주는 챗봇입니다.
            이제 다음 문장에 답해주세요.
            {user_message}
            """

def add_message_to_history(history, role, content):
    history.append({"role": role, "content": content})

def generate_chat_prompt_with_history(history, user_message):
    user_prompt = create_user_chat_prompt(user_message)
    add_message_to_history(history, "user", user_prompt)
    return history

if __name__ == '__main__':
    main()
