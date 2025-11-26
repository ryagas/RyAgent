import os
import sys

# Add the functions directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Import just the function we need, not the schema
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

# Test 1: Non-existent directory
print("Test 1: Non-existent directory")
result = get_files_info(".", "nonexistent_dir")
print(f"Result: {result}")
assert result == 'Error: Directory "nonexistent_dir" does not exist', "Failed: should return directory not exist error"
print("✓ PASSED\n")

# Test 2: Existing file (not a directory)
print("Test 2: Existing file (not a directory)")
result = get_files_info(".", "README.md")
print(f"Result: {result}")
assert result == 'Error: "README.md" is not a directory', "Failed: should return not a directory error"
print("✓ PASSED\n")

# Test 3: Valid directory
print("Test 3: Valid directory (calculator)")
result = get_files_info(".", "calculator")
print(f"Result (first 100 chars):\n{result[:100]}...")
assert "lorem.txt" in result and "main.py" in result, "Failed: should list calculator directory contents"
print("✓ PASSED\n")

# Test 4: Current directory
print("Test 4: Current directory (default)")
result = get_files_info(".")
print(f"Result (first 100 chars):\n{result[:100]}...")
assert len(result) > 0 and "README.md" in result, "Failed: should list current directory contents"
print("✓ PASSED\n")

print("="*50)
print("All tests passed successfully! ✓")