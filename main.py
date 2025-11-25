import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


def main():
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )
    verbose = False
    user_prompt = None
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    model_name = "gemini-2.0-flash-001"
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
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )
    if verbose:
        print("User prompt: " + user_prompt)
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)

    if (response.function_calls != None and len(response.function_calls) > 0):
        for call in response.function_calls:
            print (f"Calling function: {call.name}({call.args})")
        print(response.text)
    else:
        print(response.text)


if __name__ == "__main__":
    main()
