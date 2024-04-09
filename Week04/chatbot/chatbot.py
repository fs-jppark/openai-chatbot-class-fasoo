import streamlit as st
import tiktoken
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from doc_loader import get_text

load_dotenv(
    dotenv_path="./env/.env",  # .env 경로를 절대 경로 또는 상대경로로 입력합니다.
    verbose=True)

from embed_store import EmbeddingStore
from open_ai_chat import chat


def main():
    st.set_page_config(page_title="", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title("_My :red[Chatbot Demo]_")  # 챗봇 제목

    embed_store = EmbeddingStore()

    with st.sidebar:
        uploaded_files = st.file_uploader("Upload your file", type=['pdf', 'docx'], accept_multiple_files=True)
        process = st.button("업로드")
        search_knowledge_base = st.checkbox("지식 데이터베이스에서 검색")

    if process:
        files_text = get_text(uploaded_files)
        chunks = get_text_chunks(files_text)

        docs = [d.page_content for d in chunks]
        embed_store.insert_document(docs)

        st.success("업로드가 완료되었습니다.", icon="✅")


    #  채팅 부분
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "당신은 jppark 의 챗봇입니다. 사람들에게 기쁨을 주는 챗봇입니다. 항상 밝고, 명랑한 어조로 대답합니다."}]

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
                if search_knowledge_base is True:
                    query_docs = embed_store.query_embedding(text=query)
                    response = chat(messages=create_messages(st.session_state.chat_history, get_prompt_refer_doc(query_docs, query)))
                else:
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


def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)


# RecursiveCharacterTextSplitter 를 이용해 chunk 리턴해보세요.
def get_text_chunks(text) -> list[Document]:
    pass

# 쿼리된 참고문서와 질문으로 프롬프트를 만들어 보세요.
def get_prompt_refer_doc(docs: dict, query: str):
    pass

if __name__ == '__main__':
    main()
