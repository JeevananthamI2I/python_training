#Decorators
def my_decorator(func):
    def wrapper():
        print("Before function execution")
        func() 
        print("After function execution")
    return wrapper

@my_decorator  # Applying the decorator
def say_hello():
    print("Hello, World!")

say_hello()

class find_odd:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        print(f"Result: {result}")
        return result*2
    
@find_odd
def get_number(a,b):
    return a+b

print(get_number(1,2))
