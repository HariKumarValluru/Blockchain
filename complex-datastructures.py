# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.

persons = [
    {
        "name": "Hari",
        "age": 28,
        "hobbies": [
            "Video Games",
            "Learning"
        ]
    },
    {
        "name": "Tej",
        "age": 19,
        "hobbies": [
            "Listening to Music"
        ]
    },
    {
        "name": "Parikshit",
        "age": 40,
        "hobbies": [
            "Yoga"
        ]
    }
]

# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).

names = [person['name'] for person in persons]
print(names)

# 3) Use a list comprehension to check whether all persons are older than 20.

all_persons = all([person['age'] > 20 for person in persons])
print(all_persons)

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).

copy_persons = [person.copy() for person in persons]
copy_persons[0]['name'] = "Sai"
print(copy_persons)
print(persons)

# 5) Unpack the persons of the original list into different variables and output these variables.
p1, p2, p3 = persons

print(p1)
print(p2)
print(p3)