from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
import os

os.environ["OPENAI_API_KEY"] = "sk-OAbZ2yRJdYz9KOC207C60e1644274dCbB029B417E246E851"

class ChatGpt:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url="https://api3.apifans.com/v1"
        )
        self.msgs = []


    def pushUserMessage(self, content: str):
        self.msgs.append({'role':'user', 'content': content})
        
    def pushSystemMessage(self, content: str):
        self.msgs.append({'role':'system', 'content': content})

    def getGptMsg(self):
        '''返回gpt的回复并自动加入当前对话列表'''
        completion = self.client.chat.completions.create(
            messages=self.msgs,
            model="gpt-3.5-turbo-1106",
        )
        receiveMsg = completion.choices[0].message.content
        self.msgs.append({'role':'system', 'content': receiveMsg})
        return receiveMsg

    def deleteMessage(self):
        self.msgs.pop()

class ragChat:
    def __init__(self) -> None:
        self.langchinChat = ChatOpenAI(
            openai_api_key="sk-OAbZ2yRJdYz9KOC207C60e1644274dCbB029B417E246E851",
            model='gpt-3.5-turbo',
            base_url="https://api3.apifans.com/v1"
        )