# Import re module
import re

# Take any string data
string = input("\nEnter a string value: ")
# Define the searching pattern
pattern = '^[A-Z]'

# match the pattern with input value
found = re.match(pattern, string)

# Print message based on the return value
if found:
    print("The input value is started with the capital letter\n")
else:
    print("You have to type string start with the capital letter\n")