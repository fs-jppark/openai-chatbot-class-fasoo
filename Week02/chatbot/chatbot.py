import streamlit as st

from open_ai_chat import chat


def main():

    st.set_page_config(page_title="연한별의 Chatbot", page_icon="🙌")  # 타이틀 정보 입력
    st.title("_연한별의 :red[Chatbot Demo]_")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "안녕하세요. 연한별의 챗봇입니다."  # 원하는 인사말을 입력합니다.
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
