import faiss
import pickle

class Faiss:

    def save_index(self,embeddings,output_path):
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        faiss.write_index(index,output_path)
        return output_path

    def search_index(self,embedding,faiss_path,match=3):
        index = faiss.read_index("toc_keyprints.faiss")
        D, I = index.search(embedding, k=match)
        return D, I