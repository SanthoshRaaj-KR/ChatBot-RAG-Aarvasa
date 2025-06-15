# app/rag_engine.py

import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGEngine:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.documents = []
        self.index = None

    def load_knowledge(self):
        # Load and chunk company info
        with open("app/company_context.txt", "r") as f:
            company_text = f.read()
            self.documents.append(("company", company_text))

        # Load property listings
        df = pd.read_csv("app/listings.csv")
        for _, row in df.iterrows():
            text = f"{row['title']} - {row['bedrooms']}BHK {row['type']} in {row['location']} for ₹{row['price']}L"
            self.documents.append(("listing", text))

    def build_index(self):
        embeddings = [self.embedder.encode(doc[1]) for doc in self.documents]
        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings))
        self.embeddings = embeddings

    def retrieve_context(self, query, top_k=4):
        query_vec = self.embedder.encode(query).reshape(1, -1)
        distances, indices = self.index.search(query_vec, top_k)

        results = [self.documents[i][1] for i in indices[0]]
        return "\n".join(results)
