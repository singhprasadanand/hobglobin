# 📚 Hobglobin Knowledge Processor

This project processes **PDF bid documents** and lets you **query key information** like deadlines, scopes, and requirements using Gemini AI and FAISS vector search.

---

## ✅ Features

- Upload PDF bid documents.
- Extract structured text based on **Table of Contents (TOC)**.
- Create text **chunks** per section.
- Generate **keyprints** using Gemini model.
- Store chunks and vectors in **FAISS** for semantic search.

---

## ▶️ How to Run the Project

1. **Install dependencies**

```bash
pip install -r requirements.txt

```
2. **Run Uvicorn**

```bash
uvicorn app.main:app --reload


