student = {
    'name':'John' , 'age':25, 
    'courses':['math','eng']
          }

#print all dict
print(student)

#print only key
print(student['name'])
print(student['courses'])

#accissing key which doesn't exists
# print(student['phone'])

#accissing key which doesn't exists with get(returns None)
#print(student.get('phone'))

#accissing key which doesn't exists with get and default value
#print(student.get('phone', 'Not found'))

#addidng a key
#student['phone']='555-555'
#print(student)

#using update method for multipule keys also adding phone
student.update({'name':'jane', 'age':26, 'phone':'555-555'})
print(student)

#remove key:vale with delete
# del student['age']

#remove key:vale with pop and store value
age = student.pop('age')
print(student)
print(age)

#print dict length
print(len(student))

#print all keys
print(student.keys())

#print all values
print(student.values())

#print all paires
print(student.items())

#loop on keys only
for key in student:
    print(key)

#loop on values only
for value in student:
    print(value)

#loop on kyes and values using items
for key,value in student.items():
    print(key,value)






