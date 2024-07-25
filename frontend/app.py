conn, cursor = 1, 1

from flask import Flask, render_template, request
import openai
import os, tempfile
import sqlite3
import calendar
import datetime
import logging,traceback
from openai import OpenAI
log = logging.getLogger('main')

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
        who      CHAR(10)  NOT NULL,
        message  CHAR(256) NOT NULL,
        datetime INT       NOT NULL
    );
    '''
    cursor.execute( sql)
    assert ( conn)
    return conn

def init_client():
    sqlfile = tempfile.NamedTemporaryFile(mode='w+b', suffix=".sqlite", dir=None)                          
    print(f"logfile : {sqlfile.name}")

    conn = init_sqlite( sqlfile.name)
    print(f"##   logfile : {sqlfile.name}")
    print(f"##   conn    : {conn}")
    assert( conn)
    assert( conn.cursor)

    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    return { "openai_client": client, 'sqlite_conn': conn, 'sqlite_cursor': conn.cursor}

res = init_client()

log.debug(f"LINE 53, openai_client : %s", res['openai_client'])
log.debug(f"LINE 54, sqlite_conn   : %s", res['sqlite_conn'])
log.debug(f"LINE 55, sqlite_cursor : %s", res['sqlite_cursor'])

def get_completion( prompt, model="gpt-3.5-turbo"):
    log.debug(f" get_completion : '%s'", prompt)
    messages = [{"role": "user", "content": prompt}]

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    sql = f" INSERT INTO ChatLog(who, message, datetime) VALUES ( 'user', '{prompt}', '{utc_time}');";
    log.info(f"LOG SQL : {sql}")

    '''
    openai.RateLimitError: Error code: 429 - 
    {'error':
       {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.',
        'type': 'insufficient_quota',
        'param': None,
        'code': 'insufficient_quota'}}

    '''

    client = res['openai_client']

    #log.debug(f" openai.ChatCompletion.create : '%s'", openai.ChatCompletion.create)
    log.debug(f" res    : '%s'", res)
    log.debug(f" client : '%s'", client)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]


app = Flask(__name__)
openai.api_key  = os.environ.get("OPENAI_API_KEY")
log.debug("OPENAI_API_KEY : '%s'", openai.api_key)

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')
    log.debug("userText : '%s'", userText)
    response = get_completion( userText)  
    return response

if __name__ == "__main__":  
    app.run(debug=True)
