from openai import OpenAI

def pushUserMessage(msgs: list, content: str):
    msgs.append({'role':'user', 'content': content})

