# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe() ” method (which prints “name” and “kind” in a sentence).

# 2) Try turning describe()  from an instance method into a class and a static method. Change it back to an instance method thereafter.

# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook() ” method to “Meat” and “clean() ” to “Fruit”.

# 4) Overwrite a “dunder” method to be able to print your “Food” class.
class Food:
    # name = ''
    # kind = ''
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
    
    def describe(self):
        print("Name: " + self.name + "\nKind: "+self.kind)
    
    def __repr__(self):
        return "Name: " + self.name +" -- Kind: "+self.kind

    # @classmethod
    # def describe(cls):
    #     print("Name: "+cls.name+"\nKind: "+cls.kind)
    
    # @staticmethod
    # def describe(name, kind):
    #     print("Name: "+name+"\nKind: "+kind)

# meals = Food("Chicken","Meat")
# meals.describe()
# Food.name = "Apple"
# Food.kind = "Fruit"
# Food.describe()
# Food.describe("Ice-cream","Dessert")
class Meat(Food):
    def cook(self):
        print("I am cooking..")

class Fruit(Food):
    def clean(self):
        print("I am cleaning..")

biryani = Meat("Chicken", "Meat")
biryani.cook()

apple = Fruit("Apple", "Fruit")
apple.clean()

print(biryani)
print(apple)