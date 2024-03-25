import streamlit as st

from open_ai_chat import chat


def main():

    st.set_page_config(page_title="My Chatbot", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title("_My :red[Chatbot Demo]_")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "안닝하세요? 챗봇입니다 ^~^"  # 원하는 인사말을 입력합니다.
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
                user_message = create_user_message(query)
                st.session_state.chat_history.append({"role": "user", "content": user_message})
                response = chat(messages=st.session_state.chat_history)

                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

def create_user_message(query):
    return f"""당신은 dduri의 챗봇입니다. 다른 사람들에게 기쁨을 주는 챗봇입니다.
    항상 밝고, 명랑한 어조로 대답합니다. 이제 아래 질문에 답변하세요.
    {query}
    """

if __name__ == '__main__':
    main()
