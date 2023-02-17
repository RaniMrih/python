#get reguest for http api get data
from requests import get
#pprint makes output cleaner
from pprint import PrettyPrinter
import os
# import json
import sys
import logging
sys.path.append('c:/Users/rmrih/Rani_GitHub/python/Simple_Scripts_trainning/')
from general_classes import bcolors as C


#------------------------------------------difine logger
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

#---------------------------------------- define
printer = PrettyPrinter()
BASE_URL = 'https://api.coingecko.com/'
All_COINS = 'api/v3/coins/markets?vs_currency=usd&per_page=100&page=1'
EXCHANGE_RATE = 'api/v3/exchange_rates'
FULL_URL = BASE_URL + All_COINS
EXCHANGE_URL = BASE_URL + EXCHANGE_RATE

#----------------------------- change directory to the script path
# SCRIPT_PATH = 'c:/Users/rmrih/Rani_GitHub/python/Simple_Scripts_trainning/Currency_convert_project/'
# os.chdir(SCRIPT_PATH)
# print(os.getcwd())

#-------------------------------------------------- get all coins value req ---------------------------------------------
def get_currencies():
    data = get(FULL_URL).json()
    #if want to write data to a file
    # with open("currencies_data.txt", "w") as f:
    #     json.dump(data, f)
    data = list(data)
    return data

#-------------------------------------------------- get exchange value req ---------------------------------------------
def get_exchange():
    data = get(EXCHANGE_URL).json()
    data = dict(data)
    return data

#--------------------------------------- def loop on dict and print readable output ------------------------------------
def print_currencies(currencies):
    for currency in currencies:
        name = currency['name']
        _id = currency['id']
        symbol = currency.get('symbol',"")
        price = currency['current_price']
        print('Name: {} - Id: {} - symbol: {} - price: {} $'.format(name, _id, symbol, price))

#--------------------------------------- def loop on nested dict find currency value ------------------------------------
def get_currency_value(name,exchange):
    for key , value in exchange['rates'].items():
        if value['name'].lower() == name or value['unit'].lower() == name:
            # print(value['name'].lower())
            # print('Bitcoin to {} value is: {}'.format(name,value['value']))
            logger.debug('Bitcoin to {} value is: {}'.format(name,value['value']))
            logger.info('Bitcoin to {} value is: {}'.format(name,value['value']))
            logger.error(C.RED + 'Bitcoin to {} value is: {} '.format(name,value['value'])  + C.ENDC)


        #    print(name)
        # if value == name:
        #     print value['rates']['value']

#----------------------------------------------------- main -------------------------------------------------------------
def main():
    #change the working directory to the file path
    path=os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)
    print('- Current working directory {}'.format(os.getcwd()))


#------------------------------------------- def start running the program ----------------------------------------------
def run():
    print('\nWelcome to crypto currency convertor program')
    print('* List - Show all currences avilable')
    print('* Rate - Show currency value relative to BTC\n')
    print('- Retreving data from {} ... '.format(BASE_URL))
    currencies = get_currencies()
    # printer.pprint(data)
    exchange = get_exchange()
    # printer.pprint(exchange)
    
    while True:
        command = input('Enter a command (q to quit) : ').lower()
        if command == 'q':
            print('Exiting...\n')
            sys.exit(0)
        elif command == 'list':
            print_currencies(currencies)
        elif command == 'rate':
            while True:
                choise = input('Enter currency name or unit (i.e btc): ').lower()
                if choise == '':
                    print('Enter valid currency name or "list" to show all')
                elif choise == 'list':
                    print_currencies(currencies)
                else:
                    currency_value_to_btc = get_currency_value(choise , exchange)

#-------------------------------------------------------- Start -----------------------------------------------------
if __name__ == '__main__':
    main()
    run()



    


