import streamlit as st

from open_ai_chat import chat


def main():
    st.set_page_config(page_title="나만의 챗봇", page_icon="🙏")  # 타이틀 정보 입력
    st.title("_My :red[Chatbot Demo]_")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "당신은 박영우의 챗봇입니다. 당신은 인스타 문의 양식으로 대답합니다. 인스타 문의 양식이란, 대답에 이모티콘 최소 5개 이상을 포함해야합니다. 모든 대답엔 인사 -> 안부 -> 칭찬 -> 용건 -> 응원 의 형태로 3줄 이상 대답해야합니다."}]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "안녕하세요? 저는 인스타 문의 양식을 지키며 말하는 예의 바른 챗봇입니다.🙏🙏🙏🙏🙏"  # 원하는 인사말을 입력합니다.
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
