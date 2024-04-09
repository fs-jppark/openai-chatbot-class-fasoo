import os

import chromadb
import chromadb.utils.embedding_functions as embedding_functions

OPEN_AI_KEY = os.getenv("OPEN_AI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "my_knowledge"


# Chroma 를 이용해 벡터스토어를 만들어주세요.
class EmbeddingStore:
    _chroma_client = chromadb.Client()

    def __init__(self, api_key=OPEN_AI_KEY, embedding_model=EMBEDDING_MODEL):
        super().__init__()

    def embedding(self, doc):
        pass
    def query_embedding(self, text, n_results=10):
        pass
    def insert_document(self, docs):
        pass
