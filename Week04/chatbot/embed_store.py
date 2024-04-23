import os

import chromadb
import chromadb.utils.embedding_functions as embedding_functions

OPEN_AI_KEY = os.getenv("OPEN_AI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "my_knowledge"


# Chroma 를 이용해 벡터스토어를 만들어주세요.
class EmbeddingStore:

    def __init__(self, api_key=OPEN_AI_KEY, embedding_model=EMBEDDING_MODEL):
        super().__init__()

        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPEN_AI_KEY,
            model_name=EMBEDDING_MODEL
        )

        self._chroma_client = chromadb.Client()
        self.collection = self._chroma_client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=self.openai_ef)
        self.embedding_model = EMBEDDING_MODEL

    def embedding(self, doc):
        return self.openai_ef(doc)[0]

    def query_embedding(self, text, n_results=10):
        query_vector = self.embedding(text)
        response = self.collection.query(query_embeddings=query_vector, n_results=n_results, include=['documents', 'distances'])
        return response

    def insert_document(self, docs):
        for idx, data in enumerate(docs):
            self.collection.add(documents=data[0], ids=f"idx-{idx}")
