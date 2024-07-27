from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI( api_key=api_key )

@app.get("/chat")
@app.post("/chat")
async def chat( query: str, model: str | None = None):
    if not( bool(model)): model = "gpt-3.5-turbo"
    if model not in [ "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-1106", "gpt-4o-mini"]:
        model = "gpt-3.5-turbo"
    print("client : ", client)
    print("llmmodel : ", model)

    response = client.chat.completions.create(
        model = model,
        messages = [{ "role": "system", "content": query }]
    )

    if response and response.choices and response.choices[0]:
        content = response.choices[0].message.content
        return {"llmmodel": model, "query":query, "content": content }
    else:
        return {"llmmodel": model, "query":query, "content": "" }
