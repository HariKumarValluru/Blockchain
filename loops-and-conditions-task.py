# Create a list of names and use a for loop to output the length of each name (len() ).
names = ["Hari", "Anil", "Hanuma", "Tej Sai"]

for name in names:
    print(name + " - " , len(name))
print("-"*30)
# Add an if  check inside the loop to only output names longer than 5 characters.
for name in names:
    if len(name) > 5:
        print(name + " - " , len(name))
print("-"*30)
# Add another if  check to see whether a name includes a “n”  or “N”  character.
for name in names:
    if ("n" in name) or ("N" in name):
        print(name + " contains 'n' or 'N'")
print("-"*30)
# Use a while  loop to empty the list of names (via pop() )
while names:
    print(names)
    names.pop()

print(names)