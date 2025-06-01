PDF_UPLOAD_DIR = "uploads/pdfs"
FAISS_PATH = "dummy_db/faiss/bid_embed.faiss"
METADATA_PATH = "dummy_db/faiss/bid_embed_metadata.pkl"
KEYDB = "dummy_db/keyprints.json"

#Prompt
KEYPRINTS = "Extract the most important keywords or key points from this heading or section path:\n\n'{}'\n\nReturn a concise version in 1-2 lines."
CHAT = """
You are an assistant for processing bid documents.

Document Snippet:
"{chunks}"

Now answer: {query}
"""
