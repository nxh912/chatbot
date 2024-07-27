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
log = logging.getLogger('main')
log.setLevel( logging.INFO)

global model
model="gpt-3.5-turbo"

def init_mongo():
    uri = "monodb://nxh912@chatbot.gnjxjtw.mongodb.net/?retryWrites=true&w=majority&appName=ChatBot"
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        log.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        log.info(e)
    return client

def init_sqlite( sqlfile) : 
    con = sqlite3.connect( sqlfile)
    cursor = con.cursor()
    conn = con
    assert(conn)
    assert(cursor)

    cursor.execute("DROP TABLE IF EXISTS ChatLog")

    #Creating table as per requirement
    sql = '''
    CREATE TABLE ChatLog(
        message  CHAR(1024) NOT NULL,
        datetime INT       NOT NULL
    );
    '''
    cursor.execute( sql)
    assert ( conn)
    return conn,cursor

def init_client():
    sqlfile = tempfile.NamedTemporaryFile(mode='w+b', suffix=".sqlite", dir=None)                          

    conn, cursor = init_sqlite( sqlfile.name)
    print(f"##   sqlfile : {sqlfile.name}")
    print(f"##   conn    : {conn}")
    print(f"##   cursor  : {cursor}")
    assert( conn)
    assert( cursor)
    api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI( api_key=api_key )

    mongo_client = None
    #mongo_client = init_mongo()
    return { "openai_client": client,
             'sqlite_conn': conn, 'sqlite_cursor': cursor,
             'mongo_conn': mongo_client}

res = init_client()

log.info(f"LINE 53, openai_client : %s", res['openai_client'])
log.info(f"LINE 54, sqlite_conn   : %s", res['sqlite_conn'])
log.info(f"LINE 55, sqlite_cursor : %s", res['sqlite_cursor'])
log.info(f"LINE 69, mongo_conn : %s", res['mongo_conn'])

def get_completion( prompt, modelText):
    # gpt-3.5-turbo or gpt-3.5-turbo-0125 / gpt-3.5-turbo-16k / gpt-3.5-turbo-1106 / gpt-4o-mini
    client = res['openai_client']
    sqlite = res['sqlite_conn']
    cursor = res['sqlite_cursor']
    if not(bool(modelText)) or modelText=="None": modelText="gpt-3.5-turbo"

    log.info(f"L79 get_completion : prompt:'%s', modelText: '%s'", prompt, modelText)
    if len(prompt)< 1: return

    messages = [{"role": "user", "content": prompt}]
    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    sql_query = """INSERT INTO ChatLog
                          ( message, datetime) 
                            VALUES ('{}',{});
                """.format( prompt, date)

    #count = cursor.execute(sql_query)
    #sqlite.commit()
    log.info("SQL : %s", sql_query)
    log.info(f"1. res    : '%s'", res)
    log.info(f"2. client : '%s'", client)
    log.info(f"3. sqlite : '%s'", sqlite)
    log.info(f"4. cursor : '%s'", sqlite.cursor)
    log.info(f"5. modelText : '%s'", modelText)
    if not bool(modelText) or modelText == 'None': modelText

    response = client.chat.completions.create(
        model = modelText,
        messages = [{ "role": "system", "content": prompt }]
    )
    log.info( "messages : %s", str(messages))

    if response and response.choices and response.choices[0]:
        content = response.choices[0].message.content
        log.info( "\n\nL96 response.choices[0].message.content : \n%s", content)
        content = content.replace("\n", "\n<br/>")
        return str( content)
    else:
        return str( response)

app = Flask(__name__)
openai.api_key  = os.environ.get("OPENAI_API_KEY")
log.info( "LINE 106 ... OPENAI_API_KEY : '%s'", openai.api_key)

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response( BotAPI="http://127.0.0.1:8000/chat"):
    userText = request.args.get('msg')
    log.info("L133 userText : '%s'", userText)
    gptmodel = request.args.get('gptmodel')
    log.info("L135 gptmodel : '%s'", gptmodel)
    assert( gptmodel != 'None')
    log.info("L137 gptmodel : '%s'", gptmodel)
    print( f"API URL : {BotAPI}?query={userText}&model={gptmodel}")

    url=f"{BotAPI}?query={userText}&model={gptmodel}"
    response = requests.get( url=f"{url}")
    print( response.content)
    
    if response :
        jsonarr = json.loads( response.content)
        print(f"Bot : {jsonarr['content']}\n")
        return jsonarr['content']
    return "No response from bot"

if __name__ == "__main__":  
    app.run(debug=True)
