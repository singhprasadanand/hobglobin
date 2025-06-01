import fitz



class KnowledgeService:

    @staticmethod
    def extract_text(file_path: str, table_of_contents=False) -> str|list:
        doc = fitz.open(file_path)

        if table_of_contents:
            outline = doc.get_toc()
            contents = []

            # ToDO: to handle chunking logic for now adding page 1 content also
            page1 = doc[0]
            text = page1.get_text()
            contents.append({'level':1,'page':1,'title':text})

            for level, title, page in outline:
                contents.append({'level':level,'title':title,'page':page})
            return contents
        else:
            full_text = ""
            for i, page in enumerate(doc, start=1):
                text = page.get_text()
                full_text += f"\n--- Page {i} ---\n{text}\n"
            return full_text


    @staticmethod
    def text_chunking(raw_data: list|str) -> list[str]:
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
        raw_text = KnowledgeService.extract_text(file_path=file_path,table_of_contents=True)
        chunks = KnowledgeService.text_chunking(raw_text)
        print(chunks)

