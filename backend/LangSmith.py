from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
#llm = ChatOpenAI(api_key="sk-proj-bVPN0I5jQf1fOxBj9FceT3BlbkFJAk96OECGUMTUTRCU2wR6")
llm.invoke("how can langsmith help with testing?")

'''


import getpass
import os

#os.environ["OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage

model = ChatOpenAI(model="gpt-3.5-turbo")

model.invoke([HumanMessage(content="Hi! I'm Bob")])

'''
