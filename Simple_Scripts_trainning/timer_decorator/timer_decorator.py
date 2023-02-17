#decorator change the function behavior
#without changing the code

#------------------------------------------------ simple secorator
def func1(f):
    def wrapper(*args , **kwargs):
        print("Started")
        return_value = f(*args,**kwargs)
        print("End")
        return return_value
    return wrapper

@func1
def func2(x , y):
    print("I'm func 1")
    print(x)
    return y
    
@func1
def func3():
    print("I'm func 2")

# x = func2(5,6)
# print(x)
# func3()

#-------------------------------------------- timer decorator
import time
def timer(func):
    def wrapper(*args , **kwargs):
        start = time.time()
        return_value = func()
        total = time.time() - start
        print("Time : ", total)
        return return_value
    
    return wrapper

@timer
def test():
    for _ in range(100000):
        pass

@timer
def test2 ():
    time.sleep(2)

test()
test2()
