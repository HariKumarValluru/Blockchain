# 1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.
import random
import datetime
print(random.random())
print(random.randint(1,10))

# 2) Use the datetime library together with the random number to generate a random, unique value.
print(str(datetime.datetime.now())+str(random.random()))