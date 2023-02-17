# Initialize the list
weekdays = ["Sunday", "Monday", "Tuesday",
            "Wednesday", "Thursday", "Friday", "Saturday"]
print("Seven Weekdays are:\n")
# Iterate the list using for loop
#print with f 
print('\nprint with f')
for day in weekdays:
    print(f'The day is : {day}')

#print with .format
print('\nprint with .format')
for day in weekdays:
    print('The day is : {}'.format(day))

#print with %s or %d
print('\nprint with %s')
for day in weekdays:
    print('The day is : %s' %day)
