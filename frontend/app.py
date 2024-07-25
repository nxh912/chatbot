conn, cursor = 1, 1

#Final app.py 
#import files
from flask import Flask, render_template, request
import openai
import tempfile
import sqlite3
import calendar
import datetime
 
from openai import OpenAI


def init_sqlite( sqlfile) : 
    con = sqlite3.connect( sqlfile)
    cursor = con.cursor()
    conn = con
    assert(conn)
    assert(cursor)

    #Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS ChatLog")

    #Creating table as per requirement
    sql ='''CREATE TABLE ChatLog(
        who CHAR(10) NOT NULL,
        message CHAR(256) NOT NULL,
        datetime INT  NOT NULL
    )'''
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
        api_key="private",
    )
    return { "openai_client": client, 'sqlite_conn': conn, 'sqlite_cursor': conn.cursor}

res = init_client()

print(f"LINE 53, openai_client : {res['openai_client']}")
print(f"LINE 54, sqlite_conn   : {res['sqlite_conn']}")
print(f"LINE 54, sqlite_cursor : {res['sqlite_cursor']}")

def get_completion( prompt, model="gpt-3.5-turbo"):
    print(f"DEBUG: get_completion : '{prompt}'")
    messages = [{"role": "user", "content": prompt}]

    date = datetime.datetime.utcnow()
    utc_time = calendar.timegm(date.utctimetuple())

    sql = f" INSERT INTO ChatLog(who, message, datetime) VALUES ( 'user', '{prompt}', '{utc_time}');";
    print(f" SQL : {sql}")

    print(f"LINE_70 : DEBUG  openai.ChatCompletion.create : '{openai.ChatCompletion.create}'")
    print(f"LINE_71 : DEBUG  res : {res}")

    client = res['openai_client']
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]


app = Flask(__name__)
openai.api_key  = "<place your openai_api_key>"

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')
    print(f"userText : '{userText}'")
    response = get_completion( userText)  
    #return str(bot.get_response(userText)) 
    return response


if __name__ == "__main__":  
    app.run(debug=True)
