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
        '''返回gpt的回复（消耗tokens次数！别乱用）'''
        return self.client.chat.completions.create(
            messages=self.msgs,
            model="gpt-4o",
        ).choices[0].message.content

    def getandpushGptMsg(self):
        '''返回gpt的回复并自动加入当前对话列表（消耗tokens次数！别乱用）'''
        completion = self.client.chat.completions.create(
            messages=self.msgs,
            model="gpt-4o",
        )
        receiveMsg = completion.choices[0].message.content
        self.pushSystemMessage(receiveMsg)
        return receiveMsg

    def deleteMessage(self):
        self.msgs.pop()
        
    def MessageHistory(self):
        for msg in self.msgs:
            print(msg['role'] + ': ' + msg['content'])

class ragChat:
    def __init__(self) -> None:
        self.langchinChat = ChatOpenAI(
            openai_api_key="sk-OAbZ2yRJdYz9KOC207C60e1644274dCbB029B417E246E851",
            model='gpt-4o',
            base_url="https://api3.apifans.com/v1"
        )
        self.msgs = []
        self.roles = []
    
    def pushUserMessage(self, content: str):
        self.msgs.append(HumanMessage(content=content))
        self.roles.append('User')
        
    def pushSystemMessage(self, content: str):
        self.msgs.append(AIMessage(content=content))
        self.roles.append('AI')

    def getGptMsg(self):
        '''返回gpt的回复（消耗tokens次数！别乱用）'''
        return self.langchinChat(self.msgs).content

    def getandpushGptMsg(self):
        '''返回gpt的回复并自动加入当前对话列表（消耗tokens次数！别乱用）'''
        receiveMsg = self.langchinChat(self.msgs).content
        self.pushSystemMessage(receiveMsg)
        return receiveMsg

    def deleteMessage(self):
        self.msgs.pop()

    def MessageHistory(self):
        i = 0
        for msg in self.msgs:
            print(self.roles[i] + ': ' + msg.content)
            print('*************************************************')
            i += 1
    
    def clearHistory(self):
        while (len(self.msgs)):
            self.msgs.pop()