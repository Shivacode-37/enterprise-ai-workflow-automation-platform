from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


BASE_DIR = Path(__file__).resolve().parents[1]
POLICY_PATH = BASE_DIR / "knowledge" / "it_asset_policy.txt"


def create_policy_retriever():
    loader = TextLoader(
        str(POLICY_PATH),
        encoding="utf-8",
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        api_key=settings.openai_api_key,
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="it_asset_policies",
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 3},
    )
