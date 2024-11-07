import os
import os.path as osp
import sys
import logging
import csv
import io
import base64
import ast

from tqdm import tqdm
import json


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas  
from scipy.interpolate import griddata
from scipy.interpolate import RegularGridInterpolator



from flask import Flask, jsonify, request, render_template
from flask_cors import CORS 
from ragutils import ChatGpt, ragChat
from langchain_openai import ChatOpenAI
import importlib
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.documents import Document
import chromadb.api

# os.environ["OPENAI_API_KEY"] = "sk-OAbZ2yRJdYz9KOC207C60e1644274dCbB029B417E246E851"
# loader = PyPDFLoader("Baichuan2.pdf")

# pages = loader.load_and_split()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap = 50,
# )

# docs = text_splitter.split_documents(pages)

# print(len(docs))
# embed_model = OpenAIEmbeddings(model="text-embedding-3-large", base_url="https://api3.apifans.com/v1")
# vectors = embed_model.embed_documents(["hello", "goodbye"])
# # Showing only the first 3 coordinates
# print(len(vectors))
# print(vectors[0][:3])
# embed_model
# vectorstore = Chroma.from_documents(documents=docs, embedding=embed_model, collection_name="openai_embed")

embed_model = OpenAIEmbeddings(base_url="https://api3.apifans.com/v1")
query = "the plane has wings"
# for key in discriptionDocs.keys():
#     localDBvectorstore[key] = 
localvs = Chroma(persist_directory='./discription_embedding/airplane', embedding_function=embed_model, collection_name="model_discription_embed")
result = localvs.similarity_search(query, k = 5)
print (result)