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
    model_class = 'airplane'
    k = int(request.form.get('k'))
    embed_model = OpenAIEmbeddings(base_url="https://api3.apifans.com/v1")
    print (discription_filepath + '/' + model_class)
    localvs = Chroma(persist_directory=discription_filepath + '/' + model_class, embedding_function=embed_model, collection_name="model_discription_embed")
    result = localvs.similarity_search(query, k = k)
    print (result)
    res = [p.page_content for p in result[-5:]]
    
    return jsonify([p.page_content for p in result])
    # return jsonify('res')

@app.route('/get_keywords', methods=['GET', 'POST'])
def get_keywords():
    global Part2Discription
    query = request.form.get('prompt')
    model_class = request.form.get('modelclass')
    model_class = 'airplane'
    ragClient = ragChat()
    print(Part2Discription[model_class])
    prompt_template2 = f"""请基于以下数据库回答问题，该数据库为一个字典结构，键值为cap类物体拥有的部位名称，值为该部位可用的描述信息。你需要返回的内容格式为 {{\"answer\": \"...\", \"discription\": {{\"...\":[\"...\"], \"...\":[\"...\"], \"...\":[\"...\"]}}}}，\"answer\"为你对query的回答，\"discription\"为数据库中与query最相关的三个部位，每个部位提供三条描述内容，不要翻译。如果用户提问与物品部位与描述无关，则\"discription\"的值为空即可，以英文形式返回内容中原文，不要以代码形式返回

    内容:
    {Part2Discription[model_class]}
    query:
    {query}
    """
    ragClient.pushUserMessage(prompt_template2)
    answer = ragClient.getGptMsg()



    ragClient.clearHistory()
    print (answer)



    return jsonify(answer)



if __name__ == '__main__':
    global Part2Discription
    Part2Discription = {}
    with open('Part2Discription', 'r') as f:
        Part2Discription = json.load(f)
    app.debug = True
    parser = argparse.ArgumentParser(description='Run Flask application.')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port to run the application')
    args = parser.parse_args()
    app.run(port=args.port)