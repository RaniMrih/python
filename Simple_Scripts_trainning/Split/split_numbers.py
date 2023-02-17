import sys
import os
import logging
sys.path.append('c:/Users/rmrih/Rani_GitHub/python/Simple_Scripts_trainning/')
import general_classes as G
#-------------------create logger from general classes
logger = G.create_logger(os.path.basename(__file__),'sample.log')

#-------------------run the split method and mesure time with decorator
@G.timer
def run(user_input):
    clean_names = list()
    numbers_list = user_input.split(',')

    for _ in numbers_list:
        if '[' in _ or ']' in _:
            tmp = _.split('[')
            server_name = tmp[0]
            servers_numbers = tmp[1].strip(']')
            first_num = servers_numbers.split('-')[0]
            second_num = servers_numbers.split('-')[1]
            for i in range(int(first_num) , int(second_num)+1):
                if len(str(i)) == 1:
                    i = '00'+str(i)
                elif len(str(i)) == 2:
                    i = '0'+str(i)
                SERVER = server_name + str(i)   
                clean_names.append(SERVER)         
        else:
                clean_names.append(_) 
    return clean_names     

#---------------------------------------- Start user input -----------------------------------------
if __name__ == '__main__':
    user_input = input(G.bcolors.GREEN + 'Enter servers saparated by "," or range like: server-[xxx] : ' + G.bcolors.ENDC)
    clean_names = run(user_input)
    logger.info(clean_names)




 

             
