import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
		name="get_files_info",
		description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
		parameters=types.Schema(
				type=types.Type.OBJECT,
				properties={
						"directory": types.Schema(
								type=types.Type.STRING,
								description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
						),
				},
		),
)

def get_files_info(working_directory, directory="."):
	working_dir_abs = os.path.abspath(working_directory)
	full_path = os.path.abspath(os.path.join(working_directory, directory))
	
	try:
		common_path = os.path.commonpath([working_dir_abs, full_path])
		if common_path != working_dir_abs:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	except ValueError:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	
	if not os.path.exists(full_path):
		return f'Error: Directory "{directory}" does not exist'
	
	if not os.path.isdir(full_path):
		return f'Error: "{directory}" is not a directory'
	
	files_info = ""
	try:
		for file in os.listdir(full_path):
			file_path = os.path.join(full_path, file)
			files_info += f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"
	except Exception as e:
		return f"Error: {e}"
	return files_info
