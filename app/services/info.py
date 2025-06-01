import os
import pickle
from app.utils import embedding, faiss_handler, gemini_handler
from app.config import FAISS_PATH, METADATA_PATH, CHAT

def process_query(query:str):
    embed_query = embedding.SentenceEmbedder().encode(query)

    #now search in faiss to find semantic similarity
    faiss_db_path = os.path.join(os.getcwd(),FAISS_PATH)
    D, I = faiss_handler.Faiss().search_index(embed_query,faiss_db_path)

    #get embedding similar to matched vectors
    metadata_path = os.path.join(os.getcwd(),METADATA_PATH)
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)

    # get matched chunk text
    matched = []
    for i in I[0]:
        matched.append(metadata[i])


    # now pass this matched text as context to prompt for query
    prompt = CHAT.format(chunks="\n".join(matched),query=query)
    model = gemini_handler.CallGemini()
    model_output = model.generate_content(prompt)

    return model_output