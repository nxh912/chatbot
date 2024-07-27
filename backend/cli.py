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

    while True:
        print("Enter text to Bot >>> ", end=""),
        user_input = input()
        if not(user_input): break

        #query = {'query': "good morning", 'model': "gpt-3.5-turbo-16k"}

        MODEL="gpt-3.5-turbo"
        querystr=f"query={urllib.parse.quote(user_input)}&model={urllib.parse.quote(MODEL)}"
        print(f"ChatBotAPI = {ChatBotAPI}")
        print(f"querystr = {querystr}")
        print(f"Q : {ChatBotAPI}?{querystr}")
        response = requests.get( url=f"{ChatBotAPI}?{querystr}")
        print( response.json())
        assert(0)


        response = requests.post( url="http://127.0.0.1:8000/chat", json=params)
        print( response.json() )
        #response = requests.post( ChatBotAPI, json=query)

        assert(0)

        if response and response.choices and response.choices[0]:
            content = response.choices[0].message.content
            user_inputs.append( user_input)
            llm_outputs.append( str(content ))
            print(f"Bot : {content}\n")

    ### print inputs and LLM outputs before exit
    assert( len(user_inputs)==len(llm_outputs))
    print("\n\n=======================>\nLLM Log:")
    for i in range( len( user_inputs)):
        print(f">>> {user_inputs[i]}")
        print(f"bot: {llm_outputs[i]}\n")

if __name__ == "__main__":
    main()
