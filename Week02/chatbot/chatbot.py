import streamlit as st

from open_ai_chat import chat


def main():

    st.set_page_config(page_title="Dahee's Chatbot", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title("_Dahee :red[Chatbot Demo]_")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "안녕하세요. Dahee의 챗봇입니다. 무엇을 도와드릴까요?"  # 원하는 인사말을 입력합니다.
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
                st.session_state.chat_history.append({"role": "user", "content": query}) # user 질문 저장
                
                new_message = create_new_message(query)
                response = chat(messages=st.session_state.chat_history)
                
                st.markdown(response)

        st.session_state.chat_history.append({"role": "assistant", "content": response}) # user 질문에 대해 생성한 답변 저장
        st.session_state.messages.append({"role": "assistant", "content": response}) # 답변 전달

def create_new_message(query):
    return f"""당신은 Dahee의 챗봇입니다. 최대한 상냥하게 정확한 정보를 전달하세요.
                이제 아래 [질문]에 답변하세요.
                {query}
                """


if __name__ == '__main__':
    main()
