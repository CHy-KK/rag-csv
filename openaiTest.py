from langchain_openai import ChatOpenAI

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)



langchain_messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Knock knock."),
    AIMessage(content="Who's there?"),
    HumanMessage(content="Orange"),
]


langchinChat = ChatOpenAI(
    openai_api_key="sk-OAbZ2yRJdYz9KOC207C60e1644274dCbB029B417E246E851",
    model='gpt-3.5-turbo',
    base_url="https://api3.apifans.com/v1"
)

print('-------------------------------')
res = langchinChat(langchain_messages)
print (res.content)
print('-------------------------------')