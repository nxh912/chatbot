# chatbot

## Overview
You have been tasked to create an MVP application to facilitate the utilization of LLMs. The
MVP comprises:

1. Task 1: A backend component that interacts with the LLMs
1. Task 2: A frontend component that presents LLM data to the users

## Installation
Running ChatBot (CLI) on port 8000:
 - ```cd backend```
 - ```fastapi dev ChatBotREST.py```
 
Running ChatBot (UI) on port 5000:
 - ```cd frontend```
 - ```export OPENAI_API_KEY=sk-None-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ```
 - ```python3 app.py```
 - Point the browser to ```http://127.0.0.1:5000```

## Running Backend

 ```
 cd backend/
 fastapi dev backend/ChatBotREST.py
 ```

```
### curl 'http://127.0.0.1:8000/chat?query=good+morning&model=gpt-3.5-turbo-16k'
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< date: Sat, 27 Jul 2024 05:25:49 GMT
< server: uvicorn
< content-length: 109
< content-type: application/json
< 
* Connection #0 to host 127.0.0.1 left intact
{
    "llmmodel":"gpt-3.5-turbo-16k",
    "query":"good morning",
    "content":"Good morning! How can I assist you today?"
}
 ```
## Running Frontend

