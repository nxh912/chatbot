conn, cursor = 1, 1

from flask import Flask, render_template, request
import openai
import os, tempfile
import sqlite3
import calendar
import datetime
import logging,traceback
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
        log.error("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        log.error(e)
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

log.error(f"LINE 53, openai_client : %s", res['openai_client'])
log.error(f"LINE 54, sqlite_conn   : %s", res['sqlite_conn'])
log.error(f"LINE 55, sqlite_cursor : %s", res['sqlite_cursor'])
log.error(f"LINE 69, mongo_conn : %s", res['mongo_conn'])

def get_completion( prompt, modelText="gpt-3.5-turbo"):
    # or gpt-3.5-turbo-0125 / gpt-3.5-turbo-16k / gpt-3.5-turbo-1106 / gpt-4o-mini
    log.error(f"L79 get_completion : prompt:'%s', modelText: '%s'", prompt, modelText)
    if len(prompt)< 1: return
    messages = [{"role": "user", "content": prompt}]

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    client = res['openai_client']
    sqlite = res['sqlite_conn']
    cursor = res['sqlite_cursor']

    sql_query = """INSERT INTO ChatLog
                          ( message, datetime) 
                            VALUES ('{}',{});
                """.format( prompt, date)
    
    if not modelText: modelText="gpt-3.5-turbo"

    #count = cursor.execute(sql_query)
    #sqlite.commit()
    log.error("SQL : %s", sql_query)

    #log.error(f" openai.ChatCompletion.create : '%s'", openai.ChatCompletion.create)
    log.error(f"1. res    : '%s'", res)
    log.error(f"2. client : '%s'", client)
    log.error(f"3. sqlite : '%s'", sqlite)
    log.error(f"4. cursor : '%s'", sqlite.cursor)
    log.error(f"5. modelText : '%s'", modelText)

    response = client.chat.completions.create(
        model = modelText,
        messages = [{ "role": "system", "content": prompt }]
    )
    log.error( "messages : %s", str(messages))

    if response and response.choices and response.choices[0]:
        content = response.choices[0].message.content
        log.error( "\n\nL96 response.choices[0].message.content : \n%s", content)
        content = content.replace("\n", "\n<br/>")
        return str( content)
    else:
        return str( response)

app = Flask(__name__)
openai.api_key  = os.environ.get("OPENAI_API_KEY")
log.error( "LINE 106 ... OPENAI_API_KEY : '%s'", openai.api_key)

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    log.error("L133 userText : '%s'", userText)
    gptmodel = request.args.get('gptmodel')
    log.error("gptmodel : '%s'", gptmodel)
    assert( gptmodel != 'None')
    log.error("L137 gptmodel : '%s'", gptmodel)
    response = get_completion( userText, gptmodel)
    return response

if __name__ == "__main__":  
    app.run(debug=True)
