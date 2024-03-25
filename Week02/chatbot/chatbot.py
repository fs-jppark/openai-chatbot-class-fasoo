import csv
import streamlit as st

from open_ai_chat import chat

def create_user_message(query):
    return f"""python에서 {query}"""

def main():

    st.set_page_config(page_title="Phtyon Helper", page_icon="ICON")  # 타이틀 정보 입력
    st.title("Phtyon 관련 내용 질의하세요")  # 챗봇 제목

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role":"assistant", "content":"당신은 챗봇입니다."}
        ]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role":"assistant", "content":"안녕하세요. 파이썬 쳇봇입니다"}
            ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    with open('my_data.csv', 'r', encoding='utf-8') as csvfile:
        for line in csvfile:
            #print(line.strip())    
            result = line.split(",")[1]
            st.markdown(result)
            print(result)


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

        with open('my_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            # writer 객체 생성
            writer = csv.writer(csvfile)

            writer.writerow(['assistant', response])


if __name__ == '__main__':
    main()
