import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
	name="run_python_file",
	description="Executes the specified python file, constrained to the current working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path of the target file, relative to the working directory.",
			),
			"args": types.Schema(
				type=types.Type.ARRAY,
				description="List of optional arguments to be passed to the target python script as part of its execution.",
				items=types.Schema(type=types.Type.STRING)
			),
		},
		required=["file_path"],
	),
)

def run_python_file(working_directory, file_path, args=[]):
	working_dir_abs = os.path.abspath(working_directory)
	full_path = os.path.abspath(os.path.join(working_directory, file_path))

	try:
		common_path = os.path.commonpath([working_dir_abs, full_path])
		if common_path != working_dir_abs:
			return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

	# is it a directory?
	if os.path.isdir(full_path):
		return f'Error: File not found or is not a regular file: "{full_path}"'

	# Check if file exists
	if not os.path.isfile(full_path):
		return f'Error: File "{file_path}" not found.'
	
	# not a Python file
	if not file_path.endswith('.py'):
		return f'Error: "{file_path}" is not a Python file.'
	
	# run the file
	try:
		process = subprocess.run(
			["python", full_path] + args,
			timeout = 30,
			capture_output = True,
			cwd = working_dir_abs
			)
	except Exception as e:
		return f"Error: executing Python file: {e}"
	
	if process.stdout == '':
		return 'No output produced.'
	return_info = 'Process exited with code' + process.returncode if process.returncode != 0 else ''
	
	return process.stdout + process.stderr
