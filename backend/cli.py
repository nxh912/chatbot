import argparse, os
import requests, urllib.parse, json

from pathlib import Path
from openai import OpenAI

ChatBotAPI='http://127.0.0.1:8000/chat'

parser = argparse.ArgumentParser()
parser.add_argument("--llm", default='gpt-3.5-turbo')

args = parser.parse_args()
#print(args)
#print( args.llm)

def main():
    user_inputs = []
    llm_outputs = []
    api_key = os.environ.get("OPENAI_API_KEY")
    assert( api_key)
    client = OpenAI( api_key=api_key )

    print("Type your query to Chat Bot, (<Enter> to quit)"),

    while True:
        print(">>> ", end=""),
        user_input = input()
        if not(user_input): break

        #query = {'query': "good morning", 'model': "gpt-3.5-turbo-16k"}

        MODEL="gpt-3.5-turbo"
        querystr=f"query={urllib.parse.quote(user_input)}&model={urllib.parse.quote(MODEL)}&temperature=0.5"

        response = requests.get( url=f"{ChatBotAPI}?{querystr}")
        if response :
            jsonarr = json.loads( response.content)
            #print("RESPONSE: ",  jsonarr['content'])    
            user_inputs.append( user_input)
            llm_outputs.append( str( jsonarr['content'] ))
            print(f"Bot : {jsonarr['content']}\n")

    ### print inputs and LLM outputs before exit
    assert( len(user_inputs)==len(llm_outputs))
    print("\n\n=======================>\nAI Chat Log:\n")
    for i in range( len( user_inputs)):
        print(f"ME : {user_inputs[i]}")
        print(f"BOT: {llm_outputs[i]}\n")

if __name__ == "__main__":
    main()
