import os
from functions.get_files_info import get_files_info

result = get_files_info("calculator", ".")
print("Result for current directory:")
for line in result.split("\n"):
    print(" " + line)
result = get_files_info("calculator", "pkg")
print("Result for 'pkg' directory:")
for line in result.split("\n"):
    print(" " + line)
result = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
for line in result.split("\n"):
    print(" " + line)
result = get_files_info("calculator", "../")
print("Result for '../' directory:")
for line in result.split("\n"):
    print(" " + line)
