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
import argparse

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas  
from scipy.interpolate import griddata
from scipy.interpolate import RegularGridInterpolator
import chromadb.api
from werkzeug.routing import BaseConverter

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

app = Flask(__name__)
CORS(app)

discription_filepath = './discription_embedding'
'./discription_embedding/airplane'
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        
        # 将接收的第1个参数当作匹配规则进行保存
        self.regex = args[0]

app.url_map.converters['re'] = RegexConverter

@app.route('/get_similar_prompts', methods=['GET', 'POST'])
def get_similar_prompts():
    query = request.form.get('prompt')
    model_class = request.form.get('modelclass')
    k = int(request.form.get('k'))
    embed_model = OpenAIEmbeddings(base_url="https://api3.apifans.com/v1")
    print (discription_filepath + '/' + model_class)
    localvs = Chroma(persist_directory=discription_filepath + '/' + model_class, embedding_function=embed_model, collection_name="model_discription_embed")
    result = localvs.similarity_search(query, k = k)
    print (result)
    res = [p.page_content for p in result[-5:]]
    
    # return jsonify([p.page_content for p in result])
    return jsonify(res)



if __name__ == '__main__':
    app.debug = True
    parser = argparse.ArgumentParser(description='Run Flask application.')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port to run the application')
    args = parser.parse_args()
    app.run(port=args.port)