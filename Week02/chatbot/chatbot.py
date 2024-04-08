import streamlit as st
import os

from open_ai_chat import chat
from posixpath import splitext
from langchain_text_splitters import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings


def FixedChunk():
    text_splitter = CharacterTextSplitter(
            separator="", # 분리할 문자 지정가능 (문자단위로 분리할 때 사용)
            chunk_size=50,
            chunk_overlap=5,
            length_function=len,
            is_separator_regex=False,
        )

    doc = """혁신적인 솔루션과 서비스를 제공해 온 엔터프라이즈 소프트웨어 기업인 파수는 본격적인 생성형 AI 시대를 맞아
    ▲ AI-Ready 데이터 ▲ 엔터프라이즈 LLM ▲ AI-Ready 보안 ▲ AI-Powered 애플리케이션을 AI 비전으로 삼고, 고객의 생성형 AI 활용을 돕는 AI 전문기업으로 거듭나고 있습니다.
    이와 함께, 파수는 데이터 보안 영역에서 국내를 넘어 글로벌 시장을 선도하고 있습니다.
    이 뿐만 아니라, 문서가상화 기술을 활용한 기업용 문서관리 플랫폼, 압도적인 퍼포먼스의 빅데이터 개인정보 비식별화 솔루션, 업계 최고의 컨설턴트들이 진행하는 정보보호 컨설팅, 인공지능 기반 노트 앱, 블록체인 서비스, 그리고 자회사로 독립한 업계 선두의 애플리케이션 보안까지, 파수는 디지털 혁신을 향해 진입장벽이 높은 고부가가치 기술 분야를 꾸준히 개척해 나가고 있습니다.
    """

    texts = text_splitter.split_text(doc)

    for t in texts:
        print(f"{t} : {len(t)}")


def SplitByTokens():

    doc = """혁신적인 솔루션과 서비스를 제공해 온 엔터프라이즈 소프트웨어 기업인 파수는 본격적인 생성형 AI 시대를 맞아
    ▲ AI-Ready 데이터 ▲ 엔터프라이즈 LLM ▲ AI-Ready 보안 ▲ AI-Powered 애플리케이션을 AI 비전으로 삼고, 고객의 생성형 AI 활용을 돕는 AI 전문기업으로 거듭나고 있습니다.
    이와 함께, 파수는 데이터 보안 영역에서 국내를 넘어 글로벌 시장을 선도하고 있습니다.
    이 뿐만 아니라, 문서가상화 기술을 활용한 기업용 문서관리 플랫폼, 압도적인 퍼포먼스의 빅데이터 개인정보 비식별화 솔루션, 업계 최고의 컨설턴트들이 진행하는 정보보호 컨설팅, 인공지능 기반 노트 앱, 블록체인 서비스, 그리고 자회사로 독립한 업계 선두의 애플리케이션 보안까지, 파수는 디지털 혁신을 향해 진입장벽이 높은 고부가가치 기술 분야를 꾸준히 개척해 나가고 있습니다.
    """

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="",
        encoding_name="cl100k_base",
        chunk_size=100,
        chunk_overlap=0
    )

    texts = text_splitter.split_text(doc)

    for t in texts:
        print(f"{t} : {len(t)}")    

def RecursiveChunking():

    doc = """혁신적인 솔루션과 서비스를 제공해 온 엔터프라이즈 소프트웨어 기업인 파수는 본격적인 생성형 AI 시대를 맞아
    ▲ AI-Ready 데이터 ▲ 엔터프라이즈 LLM ▲ AI-Ready 보안 ▲ AI-Powered 애플리케이션을 AI 비전으로 삼고, 고객의 생성형 AI 활용을 돕는 AI 전문기업으로 거듭나고 있습니다.
    이와 함께, 파수는 데이터 보안 영역에서 국내를 넘어 글로벌 시장을 선도하고 있습니다.
    이 뿐만 아니라, 문서가상화 기술을 활용한 기업용 문서관리 플랫폼, 압도적인 퍼포먼스의 빅데이터 개인정보 비식별화 솔루션, 업계 최고의 컨설턴트들이 진행하는 정보보호 컨설팅, 인공지능 기반 노트 앱, 블록체인 서비스, 그리고 자회사로 독립한 업계 선두의 애플리케이션 보안까지, 파수는 디지털 혁신을 향해 진입장벽이 높은 고부가가치 기술 분야를 꾸준히 개척해 나가고 있습니다.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=120,
        chunk_overlap=5,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.split_text(doc)

    for t in texts:
        print(f"{t} : {len(t)}")

def SemanticChunking():

    doc = """혁신적인 솔루션과 서비스를 제공해 온 엔터프라이즈 소프트웨어 기업인 파수는 본격적인 생성형 AI 시대를 맞아
    ▲ AI-Ready 데이터 ▲ 엔터프라이즈 LLM ▲ AI-Ready 보안 ▲ AI-Powered 애플리케이션을 AI 비전으로 삼고, 고객의 생성형 AI 활용을 돕는 AI 전문기업으로 거듭나고 있습니다.
    이와 함께, 파수는 데이터 보안 영역에서 국내를 넘어 글로벌 시장을 선도하고 있습니다.
    이 뿐만 아니라, 문서가상화 기술을 활용한 기업용 문서관리 플랫폼, 압도적인 퍼포먼스의 빅데이터 개인정보 비식별화 솔루션, 업계 최고의 컨설턴트들이 진행하는 정보보호 컨설팅, 인공지능 기반 노트 앱, 블록체인 서비스, 그리고 자회사로 독립한 업계 선두의 애플리케이션 보안까지, 파수는 디지털 혁신을 향해 진입장벽이 높은 고부가가치 기술 분야를 꾸준히 개척해 나가고 있습니다.
    """
        
    semantic_text_splitter = SemanticChunker(OpenAIEmbeddings(api_key=os.getenv("OPEN_AI_API_KEY"), model="text-embedding-3-small"),
                                             breakpoint_threshold_type="percentile",
                                             breakpoint_threshold_amount=10
                                             )
    
    texts = semantic_text_splitter.split_text(doc)

    for t in texts:
        print(f"{t} : {len(t)}")


def main():

    # st.set_page_config()  # 타이틀 정보 입력
    # st.title()  # 챗봇 제목

    # if "conversation" not in st.session_state:
    #     st.session_state.conversation = []

    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = []

    # if "messages" not in st.session_state:
    #     st.session_state["messages"] = [{"role": "assistant",
    #                                      "content": ""  # 원하는 인사말을 입력합니다.
    #                                      }]

    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # if query := st.chat_input("질문을 입력해주세요."):
    #     st.session_state.messages.append({"role": "user", "content": query})

    #     with st.chat_message("user"):
    #         st.markdown(query)

    #     with st.chat_message("assistant"):
    #         with st.spinner("Thinking..."):
    #             response = chat(messages=[{"role":"user", "content": query}])
    #             st.markdown(response)

    #     st.session_state.messages.append({"role": "assistant", "content": response})

    print("Step1 > FixedChunk > ")

    FixedChunk()

    print("------------------------------------")

    print("Step2 > SplitByTokens > ")

    SplitByTokens()

    print("------------------------------------")

    print("Step3 > RecursiveChunking > ")

    RecursiveChunking()

    print("------------------------------------")

    print("Step4 >SemanticChunking > ")

    SemanticChunking()

    print("------------------------------------ END!")

if __name__ == '__main__':
    main()
