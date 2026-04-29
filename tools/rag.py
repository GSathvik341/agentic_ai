import os
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

PDF_URL = "https://cdn.visionias.in/value_added_material/5ca16-polity.pdf"
PDF_PATH = "data/polity.pdf"
DB_PATH = "data/chroma_db"


def download_pdf():
    if os.path.exists(PDF_PATH):
        return

    os.makedirs("data", exist_ok=True)
    r = requests.get(PDF_URL, timeout=30)
    r.raise_for_status()

    with open(PDF_PATH, "wb") as f:
        f.write(r.content)


def build_vectorstore():
    if os.path.exists(DB_PATH):
        return

    download_pdf()

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    vectordb.persist()


def search_polity_document(query: str, k: int = 4) -> str:
    try:
        build_vectorstore()

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        db = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )

        docs = db.similarity_search(query, k=k)

        if not docs:
            return "No relevant information found."

        context = "\n\n".join([d.page_content for d in docs])

        return context

    except Exception as e:
        return f"Retriever failed: {str(e)}"
