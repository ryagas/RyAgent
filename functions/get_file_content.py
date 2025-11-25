import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
	# Resolve to absolute paths to prevent directory traversal
	working_dir_abs = os.path.abspath(working_directory)
	full_path = os.path.abspath(os.path.join(working_directory, file_path))
	
	# Security check: ensure the resolved path is within the working directory
	try:
		common_path = os.path.commonpath([working_dir_abs, full_path])
		if common_path != working_dir_abs:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	except ValueError:
		# Happens on Windows when paths are on different drives
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	
	# is it a directory?
	if os.path.isdir(full_path):
		return f'Error: File not found or is not a regular file: "{full_path}"'
	
	# Check if file exists
	if not os.path.isfile(full_path):
		return f'Error: File not found: "{file_path}"'
	
	# read the file
	try:
		with open(full_path, 'r') as f:
			file_content = f.read()
	except Exception as e:
		return f'Error: Cannot read file "{full_path}": {str(e)}'
	if len(file_content) > MAX_CHARS:
		# truncate the file content
		file_content = file_content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
	return file_content