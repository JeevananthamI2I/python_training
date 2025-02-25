import os
with open("sample.txt", "w") as file:
    file.write("Hello, this is a new file.\n")
    file.write("Python makes file handling easy!")

with open("sample.txt", "r") as file:
    content = file.read() 
    print(content)

with open("sample.txt", "a") as file:
    file.write("\nAdding a new line!")

with open("sample.txt", "r") as file:
    print(file.readline())  
    print(file.readline())


if os.path.exists("sample.txt"):
    print("File exists!")
else:
    print("File not found.")


# if os.path.exists("sample.txt"):
#     os.remove("sample.txt")
#     print("File deleted!")
# else:
#     print("File does not exist.")


