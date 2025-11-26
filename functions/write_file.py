import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Write the specified content to the specified file, constrained to the current working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path of the target file, relative to the working directory.",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="The content to be written to the target file."
			),
		},
	),
)
def write_file(working_directory, file_path, content):
	full_path = os.path.join(working_directory, file_path)
	# outside the directory?
	try:
		common_path = os.path.commonpath([working_directory, full_path])
		if common_path != working_directory:
			return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	
	# is it a directory?
	if os.path.isdir(full_path):
		return f'Error: File not found or is not a regular file: "{full_path}"'
	
	# write the file
	try:
		with open(full_path, 'w') as f:
			f.write(content)
	except Exception as e:
		return f'Error: Cannot write to file "{full_path}": {str(e)}'
	return f'Successfully wrote to {file_path} ({len(content)} characters written)'