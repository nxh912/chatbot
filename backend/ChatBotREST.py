from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from starlette.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI( api_key=api_key )

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

@app.get("/chat")
@app.post("/chat")
async def chat( query: str, model: str, temperature: float):
    if not( bool(model)): model = "gpt-3.5-turbo"
    #if model not in [ "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-1106", "gpt-4o-mini"]:
    #    model = "gpt-3.5-turbo"
    print("client      : ", client)
    print("llmmodel    : ", model)
    print("temperature : ", temperature)

    response = client.chat.completions.create(
        model = model,
        messages = [{ "role": "system", "content": query }],
    )

    if response and response.choices and response.choices[0]:
        content = response.choices[0].message.content
        return { "llmmodel":    model,
                 "query":       query,
                 "content":     content}
    else:
        return {"llmmodel": model, "query":query, "content": ""}
