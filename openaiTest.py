from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
os.environ["OPENAI_API_KEY"] = "sk-OAbZ2yRJdYz9KOC207C60e1644274dCbB029B417E246E851"
loader = PyPDFLoader("Baichuan2.pdf")

pages = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
)

docs = text_splitter.split_documents(pages)

print(len(docs))
embed_model = OpenAIEmbeddings(model="text-embedding-3-large", base_url="https://api3.apifans.com/v1")
vectors = embed_model.embed_documents(["hello", "goodbye"])
# Showing only the first 3 coordinates
print(len(vectors))
print(vectors[0][:3])
# embed_model
# vectorstore = Chroma.from_documents(documents=docs, embedding=embed_model, collection_name="openai_embed")