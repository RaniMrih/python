import logging
#python Object-Oriented programming
class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELOOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'



#write the logging to a file with format (all format exists in pyrhon documintation 'Logrecord attributes')
# logging.basicConfig(filename='test.log',level=logging.INFO,
#                     format='%(asctime)s : %(levelname)s : %(message)s')

# logging.basicConfig(level=logging.INFO,
#                     format=bcolors.GREEN+ '%(asctime)s : %(levelname)s : %(message)s'+bcolors.ENDC)

#from logging advanced
#creating new specidfic logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('bcolors.GREEN+ %(asctime)s : %(levelname)s : %(message)s+bcolors.ENDC')
file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#the class itself
class Employee:

    raise_amount = 1.04
    num_of_employees = 0

    def __init__(self,user, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = user + '@nvidia.com'
        Employee.num_of_employees +=1
        logger.info('Created Employee: {} - {} from class {}'.format(self.first , self.last, 'Employee'))

    
    #class method returns employee full name
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    #class method returns the salary after raise
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amount(cls,amount):
        cls.raise_amount = amount

    @classmethod
    def from_string(cls,emp_str):
        user,first,last,pay = emp_str.split("-")
        return cls(user,first,last,pay)

    #sataticmethod checks workday, 5-6 is satarday sunday
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        else:
            return True 

#this class developer inhirit all methods from Employee its called subclass
class Developer(Employee):
    pass

if __name__ != '__main__':
    logging.info(bcolors.GREEN + "employee_class.py __name__ = {}".format(__name__) + bcolors.ENDC)

if __name__ == '__main__':
    #definning the emloyees        
    emp1=Employee('rmrih', 'Rani','Mrih',1000)
    emp2=Employee('tuser', 'Test','User',2000)

    #print from calling the class
    Employee.fullname(emp1)

    #print from calling the method of the class
    print(bcolors.BLUE +"emp1 full name = "+bcolors.ENDC,emp1.fullname())
    print(bcolors.BLUE +"emp2 full name = "+bcolors.ENDC,emp2.fullname())

    #get user as dict obj
    print(bcolors.BLUE +"emp1 dic = "+bcolors.ENDC,emp1.__dict__)
    # emp1.raise_amount=1.05
    print(bcolors.BLUE +"emp1 raise amount = "+bcolors.ENDC,emp1.raise_amount)

    #number of employees incremented once calling the class
    print(bcolors.BLUE +"Number of employees = "+bcolors.ENDC,Employee.num_of_employees)

    #change raise amount via class @method
    emp1.set_raise_amount(1.07)
    print(bcolors.BLUE +"emp1 new raise amounr = "+bcolors.ENDC,emp1.raise_amount)

    #lesson 3 split str create new instanse
    print(bcolors.BLUE +"----------------------------------"+bcolors.ENDC)
    emp_str_3 = "jdoe-John-Doe-7000"
    emp_str_4 = "ssmith-Steve-Smith-9000"

    emp3 = Employee.from_string(emp_str_3)
    emp4 = Employee.from_string(emp_str_4)

    #number of employees incremented once calling the class
    print(bcolors.BLUE +"Number of employees = "+bcolors.ENDC,Employee.num_of_employees)

    import datetime
    my_date = datetime.date(2023, 7 , 10)
    print(bcolors.BLUE +f"Is {my_date} a work day? "+bcolors.ENDC,Employee.is_workday(my_date))

    #lesson 4 Developer class inhiretance
    print(bcolors.BLUE +"----------------------------------"+bcolors.ENDC)
    dev_1 = Developer('cscaher','Corey','Scaher',50000)
    dev_2 = Developer('temployee','Test','Employee',60000)

    print(bcolors.BLUE +"dev_1 pay = "+bcolors.ENDC,dev_1.pay)
    # print("dev_2 pay = ",dev_2.pay)
    dev_1.apply_raise()
    print(bcolors.BLUE +"dev_1 after rasie = "+bcolors.ENDC,dev_1.pay)

