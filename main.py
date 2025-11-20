import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    verbose = False
    user_prompt = None
    
    if "--help" in sys.argv:
        print("Usage: python main.py <prompt> [--verbose]")
        return
    
    # First positional argument is the prompt
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("Error: Please provide a prompt!")
        exit(1)
    
    if "--verbose" in sys.argv:
        verbose = True
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages)
    if verbose:
        print("User prompt: " + user_prompt)
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)

    print(response.text)

if __name__ == "__main__":
    main()
