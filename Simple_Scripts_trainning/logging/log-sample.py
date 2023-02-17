'''
level 10 - DEBUG - detailed info for diagnosing problems
level 20 - INFO - confirmation that things are working as expected
level 30 - WARNING - somthing unexpected happened or problem
level 40 - ERROR - some functions cant be performed due to error
level 50 - CRITICAL - serious error the program unable to continue running

default logging level is worning
use logging instade of print statment
'''

import logging
import employee
#display logging on terminal
# logging.basicConfig(level=logging.DEBUG)

#write the logging to a file
# logging.basicConfig(filename='test.log',level=logging.DEBUG)

#write the logging to a file with format (all format exists in pyrhon documintation 'Logrecord attributes')
# logging.basicConfig(filename='sample.log',level=logging.DEBUG,
#                     format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')

'''program will take logging debug level from employee class
   this basic config won't over ride logging configuratios
   need to create each logger separately for this logger to work 
'''

#from logging advanced
#creating new specidfic logger and log to file with filehandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
file_handler = logging.FileHandler('sample.log')
file_handler.setFormatter(formatter)

#creating logger to log to screen with streamhandler and add both
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



#---------------------------------- functions ------------------------------------------------
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
    try:
        result = x / y
    except ZeroDivisionError:
        # logger.error('tried to divide by zero')
         logger.exception('tried to divide by zero')       
    else:
        return result

num1 = 10
# num2 = 20
num2 = 0

add_result = add(num1,num2)
# print('Add: {} + {} = {}'.format(num1, num2, add_result))
# logging.warning('Add: {} + {} = {}'.format(num1, num2, add_result))
logger.debug('Add: {} + {} = {}'.format(num1, num2, add_result))

sub_result = subtract(num1,num2)
# print('Sub: {} - {} = {}'.format(num1, num2, sub_result))
# logging.warning('Sub: {} - {} = {}'.format(num1, num2, sub_result))
logger.debug('Sub: {} - {} = {}'.format(num1, num2, sub_result))

mul_result = multiply(num1,num2)
# print('Mul: {} * {} = {}'.format(num1, num2, mul_result))
# logging.warning('Mul: {} * {} = {}'.format(num1, num2, mul_result))
logger.debug('Mul: {} * {} = {}'.format(num1, num2, mul_result))

div_result = divide(num1,num2)
# print('Div: {} / {} = {}'.format(num1, num2, div_result))
# logging.warning('Div: {} / {} = {}'.format(num1, num2, div_result))
logger.debug('Div: {} / {} = {}'.format(num1, num2, div_result))

