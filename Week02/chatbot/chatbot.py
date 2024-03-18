import streamlit as st

from open_ai_chat import chat


def main():

    st.set_page_config(page_title="", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title("_My :red[Chatbot Demo]_")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "안녕하세요? 챗봇입니다."  # 원하는 인사말을 입력합니다.
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
                response = chat(messages=[{"role":"user", "content": query}])
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    main()
