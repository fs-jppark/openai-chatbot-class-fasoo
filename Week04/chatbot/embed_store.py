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
        self._openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name=embedding_model
        )
        self._collection = self._chroma_client.get_or_create_collection(name=COLLECTION_NAME,
                                                                        embedding_function=self._openai_ef)

    def embedding(self, doc):
        return self._openai_ef(doc)[0]

    def query_embedding(self, text, n_results=10):
        embedding = self.embedding(text)
        result = self._collection.query(query_embeddings=embedding,
                                        n_results=n_results,
                                        include=['documents', 'distances', 'embeddings'])

        queried_result = []
        item_count = len(result["ids"][0])
        for i in range(item_count):
            queried_result.append({
                "id": result["ids"][0][i],
                "distances": result["distances"][0][i] if result["distances"] is not None else None,
                "embeddings": result["embeddings"][0][i] if result["embeddings"] is not None else None,
                "documents": result["documents"][0][i] if result["documents"] is not None else None
            })

        return queried_result

    def insert_document(self, docs):
        ids = [f"id-{idx}" for idx in range(len(docs))]
        self._collection.add(documents=docs, ids=ids)

