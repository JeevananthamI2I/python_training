
#positional arguments & keyword arguments
def greet(name, age):
    print(f"Hi, my name is {name} and I am {age} years old.")

def info(name, age, city):
    print(f"{name} is {age} years old and lives in {city}.")

greet("jeeva", 25) 
greet(age=25, name="jeeva")

info(name="Bob", age=30, city="Guindy")

#args
def add_numbers(*args):
    print(args)
    return sum(args)

print(add_numbers(1, 2, 3, 4, 5))

#kwargs
def show_info(**kwargs):
    print(kwargs)  # kwargs is a dictionary
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_info(name="jeeva", age=24, country="india")

#args and kwargs
def full_info(greeting, *args, **kwargs):
    print(greeting)
    print("Args:", args)
    print("Kwargs:", kwargs)

full_info("Hello!", "jeeva", 25, city="India", hobby="Dancing")

#recursive function
def factorial(n):
    if n == 0: 
        return 1
    return n * factorial(n - 1) 

print(factorial(5)) 

#lambda function
square_lambda = lambda x: x * x
print(square_lambda(5)) 

#postionall arquement and keyword arquement
def count_string():
    def count_str(*args,**kwargs):
        print("args",args)
        print("kwargs",kwargs)
    count_str(1,2,3,4,5,6,7,8,9,10,name="jeeva",age=25,place="chennai")

#anonymouns function
add = lambda x,y:x+y
print("anonymous",add(2,3))

#generator
def gen():
    gen=(i for i in range(20))
    print("generator",next(gen))
    print("generator",next(gen))
    print("generator",next(gen))

gen()

#recursion
def recurse_fun(n):
    if n==10:
        return n*n,n
    else:
        return recurse_fun(n+1)

print("recursion",recurse_fun(1))


