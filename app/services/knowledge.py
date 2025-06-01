import json
import time

import fitz
import os
import pickle
from app.config import FAISS_PATH, METADATA_PATH, KEYPRINTS, KEYDB
from app.utils import embedding, faiss_handler, gemini_handler


class KnowledgeService:

    @staticmethod
    def extract_text(file_path: str, table_of_contents=False) -> str | list:
        doc = fitz.open(file_path)

        if table_of_contents:
            outline = doc.get_toc()
            contents = []

            # ToDO: to handle chunking logic for now adding page 1 content also
            page1 = doc[0]
            text = page1.get_text()
            contents.append({'level': 1, 'page': 1, 'title': text})

            for level, title, page in outline:
                contents.append({'level': level, 'title': title, 'page': page})
            return contents
        else:
            full_text = ""
            for i, page in enumerate(doc, start=1):
                text = page.get_text()
                full_text += f"\n--- Page {i} ---\n{text}\n"
            return full_text

    @staticmethod
    def text_chunking(raw_data: list | str) -> list[str]:
        """
        Chunk text into sections like headers, body, paragraph, pages, etc.
        :param raw_data: Raw text.
        :return: List of sections.
        """

        # ToDo: for now chunking based on table of contents and taking title as knowledge
        current_titles = {}
        combined_titles = []

        for item in raw_data:
            level = item["level"]
            title = item["title"]
            current_titles[level] = title

            keys_to_delete = [key for key in current_titles if key > level]
            for key in keys_to_delete:
                del current_titles[key]

            combined = "  ".join(current_titles[i] for i in sorted(current_titles) if i <= level)
            combined_titles.append(combined)

        return combined_titles

    @staticmethod
    def process(file_path: str):
        raw_text = KnowledgeService.extract_text(file_path=file_path, table_of_contents=True)
        chunks = KnowledgeService.text_chunking(raw_text)

        # Embed each chunk in vector using sentence transformer
        embedded_text = embedding.SentenceEmbedder.encode(chunks)

        # store vectors in faiss
        faiss_db = faiss_handler.Faiss.save_index(embedded_text, os.path.join(os.getcwd(), FAISS_PATH))

        # store metadata
        metadata = {
            i: {
                "text": chunks[i]
            }
            for i in range(len(chunks))
        }
        with open(os.path.join(os.getcwd(), METADATA_PATH), "wb") as f:
            pickle.dump(metadata, f)

        # Get keyprints on each chunk from gemini and store in dummy db
        model = gemini_handler.CallGemini()
        resp = {}
        for i in range(len(chunks)):
            page_number = 'page ' + str(raw_text[i]['page'])
            model_output = model.generate_content(prompt=KEYPRINTS.format(chunks[i]))
            resp.setdefault(page_number, []).append(model_output)
            time.sleep(5)  # Todo batching logic should be implemented
        with open(os.path.join(os.getcwd(), KEYDB), 'w') as f:
            json.dump(resp, f)

        return True
