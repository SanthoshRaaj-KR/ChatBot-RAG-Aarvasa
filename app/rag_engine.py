from sentence_transformers import SentenceTransformer, util
import numpy as np
import json

class CompanyRAG:
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

class NavigationRAG:
    def __init__(self, json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.entries = [f"{entry['name']}: {entry['description']}" for entry in self.data]
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self.embedder.encode(self.entries, convert_to_tensor=True)

    def retrieve_navigation_info(self, query: str, top_k: int = 1):
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(-similarities.cpu().numpy())[:top_k]
        top_entries = [self.data[i] for i in top_indices]
        return top_entries
