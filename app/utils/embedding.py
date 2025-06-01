import numpy as np
from sentence_transformers import SentenceTransformer


class SentenceEmbedder:
    def __init__(self,model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def encode(self,input:list|str):
        if isinstance(input,str):
            input = [input]

        embeddings = self.model.encode(input, convert_to_numpy=True)
        return embeddings