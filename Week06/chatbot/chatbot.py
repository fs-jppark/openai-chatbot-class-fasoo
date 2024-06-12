import base64

import streamlit as st
import tiktoken
import whisper
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger
from st_audiorec import st_audiorec

from doc_loader import get_text
from img_loader import get_images

load_dotenv(
    dotenv_path="./env/.env",  # .env 경로를 절대 경로 또는 상대경로로 입력합니다.
    verbose=True)

from embed_store import EmbeddingStore
from open_ai_chat import chat, generate_image, generate_text_from_audio

model = whisper.load_model("base")

def main():
    st.set_page_config(page_title="", page_icon=":robot_face:")  # 타이틀 정보 입력
    st.title("_My :red[Chatbot Demo]_")  # 챗봇 제목

    embed_store = EmbeddingStore()
    place_holder = "질문을 입력해주세요."
    wav_audio_data = None

    with st.sidebar:
        uploaded_files = st.file_uploader("Upload your file", type=['pdf', 'docx', 'png'], accept_multiple_files=True)
        process = st.button("업로드")
        search_knowledge_base = st.checkbox("지식 데이터베이스에서 검색")
        st.divider()

        wav_audio_data = st_audiorec()
        audio_process = st.button("오디오로 챗하기")

        st.divider()
        uploaded_image_files = st.file_uploader("Upload your image file", type=['jpg', 'png'], accept_multiple_files=True)
        img_process = st.button("이미지 업로드")

    # 파일 업로드 버튼 처리
    if process:
        files_text = get_text(uploaded_files)
        chunks = get_text_chunks(files_text)

        if len(chunks) > 0:
            docs = [d.page_content for d in chunks]
            embed_store.insert_document(docs)
            st.success("업로드가 완료되었습니다.", icon="✅")
        else:
            st.success("추출된 텍스트가 없습니다.", icon="✅")

    # 이미지 업로드 버튼 처리
    if img_process:
        upload_images = get_images(uploaded_image_files)
        if len(upload_images) > 0:
            for fi in upload_images:
                with st.sidebar:
                    st_images = st.image(fi, width=100)

    if audio_process:
        with open("voice.wav", "wb") as v:
            v.write(wav_audio_data)

        text = generate_text_from_audio(audio_file="voice.wav", model=model)
        logger.info(f"voice text:{text}")
        process_query(embed_store, text, search_knowledge_base, uploaded_image_files)

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

    if query := st.chat_input(place_holder):
        process_query(embed_store, query, search_knowledge_base, uploaded_image_files)


def process_query(embed_store, query, search_knowledge_base, uploaded_image_files):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 이미지 설명 부분
            if len(uploaded_image_files) > 0:
                for uf in uploaded_image_files:
                    image_contents = []
                    with open(uf.name, 'rb') as f:
                        base64_string = base64.b64encode(f.read()).decode("utf-8")
                        image_contents.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_string}",
                                "detail": "low"
                            }
                        })
                text_contents = [{"type": "text", "text": query}]
                new_message = {"role": "user", "content": text_contents + image_contents}
                logger.info(f"new_message: {new_message}")
                response = chat(messages=[new_message], model="gpt-4-turbo")
            # 벡터서치
            elif search_knowledge_base is True:
                query_docs = embed_store.query_embedding(text=query)
                response = chat(messages=create_messages(st.session_state.chat_history,
                                                         get_prompt_refer_doc(query_docs, query)))
            # 일반적인 질문이 이미지를 생성하려는 의도가 있는 지 확인 후 이미지 생성 로직이면 Dall-E 호출
            else:
                logger.info("else!!")
                response = chat(
                    messages=[{"role": "user", "content": f"아래 질의는 이미지 생성 요청입니까? 예, 아니오로 대답하세요.\n {query}"}],
                    model="gpt-4-turbo")
                logger.info(f"response 1st: {response}")
                if "예" in response:
                    image_url = generate_image(prompt=query)
                    response = f"![{query}]({image_url})"
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
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        length_function=tiktoken_len
    )
    chunks = text_splitter.split_documents(text)
    return chunks


# 쿼리된 참고문서와 질문으로 프롬프트를 만들어 보세요.
def get_prompt_refer_doc(docs: dict, query: str):
    refer_doc = [item["documents"] for item in docs]
    return f"아래 참고문서를 참조해서 질문에 답변을 하세요.\n[참고문서] {refer_doc}\n[질문]{query}"


if __name__ == '__main__':
    main()
