name = input("Enter your name: ")
age = int(input("Enter your age: "))

def person():
    print("Hello my name is " + name +" and I'm ", age)

person()

def add_value(a, b):
    return a + b

print(add_value(25,20))

def calculate_decade(age):
    num_of_decades = int(age/10)
    print("Hello " + name + ", you have lived ", num_of_decades + " decades")
calculate_decade(age)