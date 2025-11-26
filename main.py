import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


def main():
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    verbose = False
    user_prompt = None
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. Prefer using tools without arguments if they are optional and none were provided.
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

    response_list = []
    if (response.function_calls != None and len(response.function_calls) > 0):
        for call in response.function_calls:
            print (f"Calling function: {call.name}({call.args})")
            function_call_result = call_function(call, verbose)
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("No response")
            else:
                response_list.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response["result"]}")
    else:
        print(response.text)

def call_function(function_call_part, verbose=False):
    func_dict = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "run_python_file" : run_python_file,
        "write_file" : write_file,
    }
    function_name = function_call_part.name
    function_args = function_call_part.args

    if function_name not in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f"Calling function: {function_name}")

    # Inject working directory as first parameter and unpack remaining args
    working_dir = os.getcwd()
    function_result = func_dict[function_name](working_dir, **function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

if __name__ == "__main__":
    main()
