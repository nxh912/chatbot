conn, cursor = 1, 1

from flask import Flask, render_template, request
import openai
import os, tempfile
import sqlite3
import calendar
import datetime
import logging,traceback
import requests, urllib.parse, json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from openai import OpenAI

#MONDB_ADMIN_USER = (os.environ['MONDB_ADMIN_USER'])
#MONDB_ADMIN_PASSWORD = (os.environ['MONDB_ADMIN_PASSWORD'])

log = logging.getLogger('main')
log.setLevel( logging.INFO)

global model
model="gpt-3.5-turbo"

def gpt_client():
    assert( conn)
    assert( cursor)
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI( api_key=api_key )
    mongo_client = None
    return { "openai_client": client,
             'mongo_conn': mongo_client}

def get_completion( prompt, modelText):
    # gpt-3.5-turbo or gpt-3.5-turbo-0125 / gpt-3.5-turbo-16k / gpt-3.5-turbo-1106 / gpt-4o-mini
    client = res['openai_client']
    if not(bool(modelText)) or modelText=="None": modelText="gpt-3.5-turbo"

    log.debug(f"get_completion : prompt:'%s', modelText: '%s'", prompt, modelText)
    if len(prompt)< 1: return

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    response = client.chat.completions.create(
        model = modelText,
        messages = [{ "role": "system", "content": prompt }]
    )

    if response and response.choices and response.choices[0]:
        content = response.choices[0].message.content
        log.debug( "response.choices[0].message.content : \n%s", content)
        content = content.replace("\n", "\n<br/>")
        return str( content)
    else:
        return str( response)

#res = gpt_client()

app = Flask(__name__)
openai.api_key  = os.environ.get("OPENAI_API_KEY")
log.debug( "OPENAI_API_KEY : '%s'", openai.api_key)

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response( BotAPI="http://127.0.0.1:8000/chat"):
    userText = request.args.get('msg')
    gptmodel = request.args.get('gptmodel')
    temperature = request.args.get('temperature')
    assert( gptmodel != 'None')
    log.debug("gptmodel : '%s'", gptmodel)
    log.debug("temperature : '%s'", temperature)
    print( f"API URL : {BotAPI}?query={userText}&model={gptmodel}&temperture={temperature}")

    url=f"{BotAPI}?query={userText}&model={gptmodel}&temperture={temperature}"
    response = requests.get( url=f"{url}")
    #print( response.content)
    
    if response :
        jsonarr = json.loads( response.content)
        print(f"Bot : {jsonarr['content']}\n")

        # db_collection.insert_one(datarow)
        return jsonarr['content']
    return "No response from bot"

if __name__ == "__main__":  
    app.run(debug=True)
