#!/usr/bin/env python
import logging
import time

#--------------------------------------- The pathes used for automation
class Pathes(object):
   grades_wb_xl = 'c:/Users/rmrih/Rani_GitHub/python/Simple_Scripts_trainning/Openpy_XL_Files/Grades.xlsx'

#--------------------------------------- colors
class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELOOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

#--------------------------------------- create logger for each script
def create_logger(script_name,log_file_name):
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(bcolors.BLUE + '%(asctime)s : %(name)s : %(levelname)s : ' + bcolors.ENDC +' %(message)s' )
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)

    #creating logger to log to screen with streamhandler and add both
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

#-------------------------------------------- timer decorator
def timer(f):
    def wrapper(*args , **kwargs):
        start = time.time()
        return_value = f(*args,**kwargs)
        total = time.time() - start
        print(bcolors.GREEN + "Running time: ", total , bcolors.ENDC)
        return return_value  
    return wrapper

