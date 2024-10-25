from openai import OpenAI

client = OpenAI(
    api_key="sk-OAbZ2yRJdYz9KOC207C60e1644274dCbB029B417E246E851",
    base_url="https://api3.apifans.com/v1"
)

def pushUserMessage(msgs: list, content: str):
    msgs.append({'role':'user', 'content': content})

def getGptMsg(msgs:list):
    '''返回gpt的回复并自动加入当前对话列表'''
    completion = client.chat.completions.create(
        messages=msgs,
        model="gpt-3.5-turbo-1106",
    )
    receiveMsg = completion.choices[0].message.content
    msgs.append({'role':'system', 'content': receiveMsg})
    return receiveMsg

def deleteMessage(msgs:list):
    msgs.pop()
