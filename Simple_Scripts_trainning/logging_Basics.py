'''
DEBUG - detailed info for diagnosing problems
INFO - confirmation that things are working as expected
WARNING - somthing unexpected happened or problem
ERROR - some functions cant be performed due to error
CRITICAL - serious error the program unable to continue running

default logging level is worning
use logging instade of print statment
'''

import logging
#display logging on terminal
# logging.basicConfig(level=logging.DEBUG)

#write the logging to a file
#logging.basicConfig(filename='test.log',level=logging.DEBUG)
import employee_class

#write the logging to a file with format (all format exists in pyrhon documintation 'Logrecord attributes')
logging.basicConfig(filename='test.log',level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s')

'''program will take logging debug level from employee class
   this basic config won't over ride logging configuratios
   need to create each logger separately for this logger to work 
'''


def add(x,y):
    '''Add function'''
    return x + y

def subtract(x,y):
    '''subtract function'''
    return x - y

def multiply(x,y):
    '''multiply function'''
    return x * y

def divide(x,y):
    '''Divide function'''
    return x / y

num1 = 10
num2 = 20

add_result = add(num1,num2)
# print('Add: {} + {} = {}'.format(num1, num2, add_result))
# logging.warning('Add: {} + {} = {}'.format(num1, num2, add_result))
logging.debug('Add: {} + {} = {}'.format(num1, num2, add_result))

sub_result = subtract(num1,num2)
# print('Sub: {} - {} = {}'.format(num1, num2, sub_result))
# logging.warning('Sub: {} - {} = {}'.format(num1, num2, sub_result))
logging.debug('Sub: {} - {} = {}'.format(num1, num2, sub_result))

mul_result = multiply(num1,num2)
# print('Mul: {} * {} = {}'.format(num1, num2, mul_result))
# logging.warning('Mul: {} * {} = {}'.format(num1, num2, mul_result))
logging.debug('Mul: {} * {} = {}'.format(num1, num2, mul_result))

div_result = divide(num1,num2)
# print('Div: {} / {} = {}'.format(num1, num2, div_result))
# logging.warning('Div: {} / {} = {}'.format(num1, num2, div_result))
logging.debug('Div: {} / {} = {}'.format(num1, num2, div_result))

