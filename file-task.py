# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.
# def options():
#     print("Menu:")
#     print("1: Enter your data")
#     print("2: Output the file data")
#     print("q: Quit!")
#     return input("Your choice: ")
# waiting = True
# while waiting:
#     user_choice = options()
#     if user_choice == "1":
#         user_input = input("Enter your data: ")
#         with open("user_data.txt", mode="a") as f:
#             f.write(user_input+"\n")
#     elif user_choice == "2":
#         with open("user_data.txt", mode="r") as f:
#             file_content = f.read()
#             print(file_content)
#     elif user_choice == "q":
#         waiting = False
#     else:
#         print("Invalid choice. Please try again!")
# 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.

# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.
import json
import pickle
def options():
    print("Menu:")
    print("1: Enter your data")
    print("2: Output the file data")
    print("q: Quit!")
    return input("Your choice: ")
data = []
waiting = True
while waiting:
    user_choice = options()
    if user_choice == "1":
        user_input = input("Enter your data: ")
        data.append(user_input)
        # 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
        with open("user_data.txt", mode="w") as f:
            f.write(json.dumps(data))
        with open("user_data.p", mode="wb") as f:
            f.write(pickle.dumps(data))
    # 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
    elif user_choice == "2":
        # 4) Adjust the logic to load the file content to work with pickled/ json data.
        with open("user_data.txt", mode="r") as f:
            file_content = json.loads(f.read())
            print("Read with JSON: ")
            print(file_content)
        with open("user_data.p", mode="rb") as f:
            file_content = pickle.loads(f.read())
            print("Read with Pickle")
            print(file_content)
    elif user_choice == "q":
        waiting = False
    else:
        print("Invalid choice. Please try again!")
# 4) Adjust the logic to load the file content to work with pickled/ json data.