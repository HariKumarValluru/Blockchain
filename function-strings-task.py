# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
def normal(arg):
    print(arg(1+4))

# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.
normal(lambda x: (x + 4))

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.

def normal2(fn, *args):
    for arg in args:
        print(fn(arg))

normal2(lambda x: x + 1,2,3,5,6,8)

# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.
def normal3(fn, *args):
    for arg in args:
        print("Result: {:^20.2f}".format(fn(arg)))

normal3(lambda x: x + 1,2,3,5,6,8)