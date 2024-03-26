import streamlit as st

from open_ai_chat import chat


def main():

    st.set_page_config(page_title="Chatbot Test", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title("_Chatbot :blue[Demo]_")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "system",
                                          "content": f"""당신은 sangwon.jo의 전문 비서 챗봇입니다. 항상 부드럽고 격식있는 어조로 대답합니다."""}]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "실습용 챗봇입니다."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("질문을 입력해주세요."):
        user_message = {"role": "user", "content": query}
        st.session_state.messages.append(user_message)
        st.session_state.chat_history.append(user_message)

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(messages=st.session_state.chat_history)
                st.session_state.chat_history.append(response)
                st.markdown(response.content)

        st.session_state.messages.append({"role": "assistant", "content": response.content})

if __name__ == '__main__':
    main()
