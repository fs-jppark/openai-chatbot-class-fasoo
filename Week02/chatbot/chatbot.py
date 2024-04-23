import streamlit as st

from open_ai_chat import chat

def main():

    st.set_page_config(page_title="My Chatbot", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title("_My :red[Chatbot Demo]_")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "당신은 박지수의 챗봇입니다. 당신은 친구같은 챗봇이므로 친구처럼 반말로 답변해줘. 이제 아래 질문에 답변하세요."}]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "안녕하세요, 챗봇입니다."  # 원하는 인사말을 입력합니다.
                                         }]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("질문을 입력해주세요."):
        st.session_state.messages.append({"role": "user", "content": query })

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(messages=create_messages(st.session_state.chat_history, query))
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({"role": "user", "content": query})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

def create_messages(old_messages, message):
    new_messages = []
    new_messages += old_messages
    new_messages.append({"role": "user", "content": message})
    print(new_messages)
    return new_messages

if __name__ == '__main__':
    main()
