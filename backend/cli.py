import argparse, os
from pathlib import Path
from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("--llm", default='gpt-3.5-turbo')

args = parser.parse_args()
#print(args)
#print( args.llm)

def main():
    user_inputs = []
    llm_outputs = []
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI( api_key=api_key )
    #print( "client : ", client)

    while True:
        print("Enter text to Bot >>> ", end=""),
        user_input = input()
        if not(user_input): break

        response = client.chat.completions.create(
            model = args.llm,
            messages = [{ "role": "system", "content": user_input }]
        )

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