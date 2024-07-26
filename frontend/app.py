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
log.setLevel( logging.INFO)

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
    return conn,cursor

def init_client():
    sqlfile = tempfile.NamedTemporaryFile(mode='w+b', suffix=".sqlite", dir=None)                          

    conn, cursor = init_sqlite( sqlfile.name)
    print(f"##   sqlfile : {sqlfile.name}")
    print(f"##   conn    : {conn}")
    print(f"##   cursor  : {cursor}")
    assert( conn)
    assert( cursor)

    client = OpenAI( api_key = os.environ.get("OPENAI_API_KEY") )
    return { "openai_client": client, 'sqlite_conn': conn, 'sqlite_cursor': cursor}

res = init_client()

log.error(f"LINE 53, openai_client : %s", res['openai_client'])
log.error(f"LINE 54, sqlite_conn   : %s", res['sqlite_conn'])
log.error(f"LINE 55, sqlite_cursor : %s", res['sqlite_cursor'])

def get_completion( prompt, model="gpt-3.5-turbo"):
    log.error(f" get_completion : '%s'", prompt)
    messages = [{"role": "user", "content": prompt}]

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    client = res['openai_client']
    sqlite = res['sqlite_conn']
    cursor = res['sqlite_cursor']
    # for m in dir( cursor ): print( f"sqlite.cursor . {m}")

    sql_query = """INSERT INTO ChatLog
                          (who, message, datetime) 
                           VALUES 
                          ('me','{}',{});""".format( prompt, date)

    #count = cursor.execute(sql_query)
    #sqlite.commit()
    log.info("SQL : %s", sql_query)

    #log.error(f" openai.ChatCompletion.create : '%s'", openai.ChatCompletion.create)
    log.error(f" res    : '%s'", res)
    log.error(f" client : '%s'", client)
    log.error(f" sqlite : '%s'", sqlite)
    log.error(f" cursor : '%s'", sqlite.cursor)

    log.error( "response : %s", str(messages))
    return "RESPONSE : " + str(messages)
    #return response.choices[0].message["content"]


app = Flask(__name__)
openai.api_key  = os.environ.get("OPENAI_API_KEY")
log.error( "LINE 106 ... OPENAI_API_KEY : '%s'", openai.api_key)

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')
    log.error("userText : '%s'", userText)
    response = get_completion( userText)  
    return response

if __name__ == "__main__":  
    app.run(debug=True)
