import os
from fastapi import APIRouter, UploadFile,File
from app.config import PDF_UPLOAD_DIR

knowledge = APIRouter()

@knowledge.post("/upload-knowledge")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}

    contents = await file.read()

    with open(os.path.join(os.getcwd(),PDF_UPLOAD_DIR,file.filename), "wb") as f:
        f.write(contents)

    """
    Also Create a record in db to store all knowledge document uploaded till date.
    This also helps if wants to present document in UI later
    """

    return {"message":"file_uploaded_successfully"}

@knowledge.get("/get-knowledge-doc/{doc_id}")
async def get_knowledge_doc(doc_id:int):
    """

    :param doc_id: int
    :return: fileresponse

    With this able to load or show any knowledge document to UI
    """
    return NotImplementedError("File response not implemented")

@knowledge.post("/process_knowledge/{doc_id}")
async def process_knowledge(doc_id:int):
    """

    :param doc_id: int
    :return: Success/Failure

    Trigger knowledge processing from the documents:
    steps:
    1. get text from pdf
    2. remove noises if require
    3. text chunking
    4. indexing in faiss
    5. while indexing store key prints in db under same doc_id
    """
    return NotImplementedError("Should Show Success/Failure once implemented")

