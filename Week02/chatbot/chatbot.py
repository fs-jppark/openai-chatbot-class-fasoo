import streamlit as st

from open_ai_chat import chat

def create_user_message(query):
    return f"""python에서 {query}"""

def main():

    st.set_page_config(page_title="Title is My Chatbot", page_icon="ICON")  # 타이틀 정보 입력
    st.title("In webbroser... What do you think about?")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role":"assistant", "content":"당신은 챗봇입니다."}
        ]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role":"assistant", "content":"This is ridicuros"},
            {"role":"assistant", "content":"한글 처리는 어떻게 되나?"},
            ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("질문을 입력해주세요."):
        reqString = create_user_message(query)
        print(reqString)
        st.session_state.messages.append({"role": "user", "content": reqString})

        with st.chat_message("user"):
            st.markdown(reqString)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(messages=[{"role":"user", "content": reqString}])
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    main()
