from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from starlette.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI( api_key=api_key )
collection_name = None

app = FastAPI()
# Set all CORS enabled origins
origins = [
    'http://127.0.0.1:8000',
    'http://127.0.0.1:5000',
    'http://localhost:8000',
    'http://localhost:5000',
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

### mango db
def mandb_connection():
    global collection_name
    MONDB_ADMIN_USER = (os.environ['MONDB_ADMIN_USER'])
    MONDB_ADMIN_PASSWORD = (os.environ['MONDB_ADMIN_PASSWORD'])
    uri = f"mongodb+srv://{MONDB_ADMIN_USER}:{MONDB_ADMIN_PASSWORD}@chatbot.6ci5bzi.mongodb.net/?retryWrites=true&w=majority&appName=chatbot"
    mongo_client = MongoClient(uri, server_api=ServerApi('1'))
    mongo_name = mongo_client['chatbot']
    collection_name = mongo_name["ChatLog"]

async def log_mangodb( model: str, query: str, content: str):
    global collection_name

    datarow = {"timestamp":  time.time(), "role" : "Chatbot", query : content}
    dbname = client['chatbot']
    print("L50 log_mangodb : dbname -> ", dbname)

    collection_name = dbname["ChatLog"]
    print("L52 log_mangodb : collection_name -> ", collection_name)

    res = collection_name.insert_one(datarow)
    print(res)

@app.get("/chat")
@app.post("/chat")
async def chat( query: str, model: str, temperature: float):
    global collection_name
    if not( bool(model)): model = "gpt-3.5-turbo"
    #if model not in [ "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-1106", "gpt-4o-mini"]:
    #    model = "gpt-3.5-turbo"

    response = client.chat.completions.create(
        model = model,
        messages = [{ "role": "system", "content": query }],
    )
    if response and response.choices and response.choices[0]:
        content = response.choices[0].message.content
        log_mangodb( model, query, content)
        return {"llmmodel": model, "query": query, "content": content}
    else:
        return {"llmmodel": model, "query":query, "content": "error"}
