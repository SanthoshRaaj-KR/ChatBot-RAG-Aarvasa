from sentence_transformers import SentenceTransformer, util
import numpy as np

class RAGEngine:
    def __init__(self, context_path: str):
        with open(context_path, "r", encoding="utf-8") as f:
            self.chunks = f.read().split("\n\n")  # Split context
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.chunk_embeddings = self.embedder.encode(self.chunks, convert_to_tensor=True)

    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> str:
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, self.chunk_embeddings)[0]
        top_indices = np.argsort(-similarities.cpu().numpy())[:top_k]
        top_chunks = "\n\n".join([self.chunks[i] for i in top_indices])
        return top_chunks
